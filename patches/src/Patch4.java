import org.objectweb.asm.ClassReader;
import org.objectweb.asm.ClassWriter;
import org.objectweb.asm.Handle;
import org.objectweb.asm.Opcodes;
import org.objectweb.asm.MethodVisitor;
import org.objectweb.asm.tree.*;

import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;

/**
 * REC beta1.6 第四次改动：新增 TaskType.SLM_TAKEOVER 枚举 + 菜单第 4 个按钮
 *
 * 用法:
 *   java Patch4 enum <TaskType.class> <out>
 *   java Patch4 switchmap <RustElytraClient$1.class> <out>
 *   java Patch4 gui <RSTScr$ciScr.class> <out>
 */
public class Patch4 {
    static final String TT = "dev/rstminecraft/TaskThread$TaskType";
    static final String TT_DESC = "Ldev/rstminecraft/TaskThread$TaskType;";
    static final String NEW_NAME = "SLM_TAKEOVER";

    public static void main(String[] args) throws Exception {
        String mode = args[0];
        byte[] cls = Files.readAllBytes(Paths.get(args[1]));
        ClassNode cn = new ClassNode();
        new ClassReader(cls).accept(cn, 0);
        switch (mode) {
            case "enum" -> patchEnum(cn);
            case "switchmap" -> patchSwitchMap(cn);
            case "gui" -> patchGui(cn);
            default -> throw new IllegalArgumentException(mode);
        }
        ClassWriter cw = new ClassWriter(ClassWriter.COMPUTE_MAXS);
        cn.accept(cw);
        Files.write(Paths.get(args[2]), cw.toByteArray());
        System.out.println("patched " + mode + " -> " + args[2]);
    }

    // ---------- 1. 枚举加常量 + $VALUES 扩容 ----------
    static void patchEnum(ClassNode cn) {
        if (cn.fields.stream().anyMatch(f -> f.name.equals(NEW_NAME))) {
            System.out.println("enum already has " + NEW_NAME);
            return;
        }
        cn.fields.add(new FieldNode(Opcodes.ACC_PUBLIC | Opcodes.ACC_STATIC | Opcodes.ACC_FINAL | Opcodes.ACC_ENUM,
                NEW_NAME, TT_DESC, null, null));

        MethodNode clinit = cn.methods.stream().filter(m -> m.name.equals("<clinit>")).findFirst().orElseThrow();
        InsnList ins = clinit.instructions;
        // 找到 INFINITY_ELYTRA 的 PUTSTATIC，在其后插入新常量构造
        AbstractInsnNode anchor = null;
        for (AbstractInsnNode a : ins) {
            if (a instanceof FieldInsnNode f && f.getOpcode() == Opcodes.PUTSTATIC
                    && f.owner.equals(TT) && f.name.equals("INFINITY_ELYTRA")) {
                anchor = a;
            }
        }
        if (anchor == null) throw new IllegalStateException("INFINITY_ELYTRA PUTSTATIC not found");

        InsnList build = new InsnList();
        build.add(new TypeInsnNode(Opcodes.NEW, TT));
        build.add(new InsnNode(Opcodes.DUP));
        build.add(new LdcInsnNode(NEW_NAME));
        build.add(new InsnNode(Opcodes.ICONST_3));       // ordinal 3
        build.add(new MethodInsnNode(Opcodes.INVOKESPECIAL, TT, "<init>", "(Ljava/lang/String;I)V", false));
        build.add(new FieldInsnNode(Opcodes.PUTSTATIC, TT, NEW_NAME, TT_DESC));
        ins.insert(anchor, build);

        // $VALUES 数组: ICONST_3 -> ICONST_4；再补一个元素
        for (AbstractInsnNode a : ins) {
            if (a instanceof TypeInsnNode t && t.getOpcode() == Opcodes.ANEWARRAY && t.desc.equals(TT)) {
                AbstractInsnNode prev = a.getPrevious();
                if (prev instanceof InsnNode i && i.getOpcode() == Opcodes.ICONST_3) {
                    ins.set(prev, new InsnNode(Opcodes.ICONST_4));
                }
            }
        }
        // $values() 是独立的合成方法：扩容并追加新元素
        MethodNode values = cn.methods.stream().filter(m -> m.name.equals("$values")).findFirst().orElse(null);
        if (values == null) throw new IllegalStateException("$values() not found");
        InsnList vins = values.instructions;
        for (AbstractInsnNode a : vins) {
            if (a instanceof TypeInsnNode t && t.getOpcode() == Opcodes.ANEWARRAY && t.desc.equals(TT)) {
                AbstractInsnNode prev = a.getPrevious();
                if (prev instanceof InsnNode i && i.getOpcode() == Opcodes.ICONST_3) {
                    vins.set(prev, new InsnNode(Opcodes.ICONST_4));
                }
            }
        }
        AbstractInsnNode ret = null;
        for (AbstractInsnNode a : vins) {
            if (a.getOpcode() == Opcodes.ARETURN) { ret = a; break; }
        }
        if (ret == null) throw new IllegalStateException("$values ARETURN not found");
        InsnList extend = new InsnList();
        extend.add(new InsnNode(Opcodes.DUP));
        extend.add(new InsnNode(Opcodes.ICONST_3));
        extend.add(new FieldInsnNode(Opcodes.GETSTATIC, TT, NEW_NAME, TT_DESC));
        extend.add(new InsnNode(Opcodes.AASTORE));
        vins.insert(ret, extend);
        System.out.println("enum: added " + NEW_NAME + " (values size 4)");
    }

    // ---------- 2. $SwitchMap 让新常量按 ELYTRA 处理 ----------
    static void patchSwitchMap(ClassNode cn) {
        MethodNode clinit = cn.methods.stream().filter(m -> m.name.equals("<clinit>")).findFirst().orElseThrow();
        InsnList ins = clinit.instructions;
        AbstractInsnNode last = null;
        for (AbstractInsnNode a : ins) {
            if (a instanceof FieldInsnNode f && f.getOpcode() == Opcodes.PUTSTATIC
                    && f.name.contains("$SwitchMap$dev$rstminecraft$TaskThread$TaskType")) {
                // 找到最后一次给这个 map 赋值的 AASTORE 的末尾（下一个 label 前）
                last = a;
            }
        }
        // 简单做法：在整个 <clinit> 末尾（最后一个 RETURN 前）插入赋值
        AbstractInsnNode ret = null;
        for (AbstractInsnNode a : ins) {
            if (a.getOpcode() == Opcodes.RETURN) { ret = a; break; }
        }
        if (ret == null) throw new IllegalStateException("no RETURN");
        InsnList add = new InsnList();
        add.add(new FieldInsnNode(Opcodes.GETSTATIC, cn.name, "$SwitchMap$dev$rstminecraft$TaskThread$TaskType", "[I"));
        add.add(new FieldInsnNode(Opcodes.GETSTATIC, TT, NEW_NAME, TT_DESC));
        add.add(new MethodInsnNode(Opcodes.INVOKEVIRTUAL, TT, "ordinal", "()I", false));
        add.add(new InsnNode(Opcodes.ICONST_3)); // 映射为 INFINITY_ELYTRA 分支
        add.add(new InsnNode(Opcodes.IASTORE));
        ins.insertBefore(ret, add);
        System.out.println("switchmap: " + NEW_NAME + " -> 1");
    }

    /** 通过 ClassWriter/ClassReader 往返深拷贝方法，得到全新的 Label 对象 */
    static MethodNode cloneMethod(MethodNode src) {
        ClassWriter cw = new ClassWriter(0);
        cw.visit(Opcodes.V21, Opcodes.ACC_PUBLIC, "tmp/Tmp", null, "java/lang/Object", null);
        MethodVisitor mv = cw.visitMethod(src.access, src.name, src.desc, src.signature,
                src.exceptions == null ? null : src.exceptions.toArray(new String[0]));
        src.accept(mv);
        mv.visitEnd();
        cw.visitEnd();
        ClassNode tmp = new ClassNode();
        new ClassReader(cw.toByteArray()).accept(tmp, 0);
        return tmp.methods.get(0);
    }

    // ---------- 3. GUI 加第 4 个按钮 ----------
    static void patchGui(ClassNode cn) {
        MethodNode ctor = cn.methods.stream().filter(m -> m.name.equals("<init>")).findFirst().orElseThrow();
        InsnList ins = ctor.instructions;

        // 数组大小 / 行数 5 -> 6
        for (AbstractInsnNode a : ins) {
            if (a instanceof InsnNode i && i.getOpcode() == Opcodes.ICONST_5) {
                ins.set(a, new IntInsnNode(Opcodes.BIPUSH, 6));
            }
        }

        // 复制 ELYTRA 按钮的 lambda
        MethodNode src = null;
        for (MethodNode m : cn.methods) {
            if (m.name.startsWith("lambda$new$")) {
                for (AbstractInsnNode a : m.instructions) {
                    if (a instanceof FieldInsnNode f && f.getOpcode() == Opcodes.GETSTATIC
                            && f.owner.equals(TT) && f.name.equals("ELYTRA")) {
                        src = m;
                        break;
                    }
                }
            }
            if (src != null) break;
        }
        if (src == null) throw new IllegalStateException("ELYTRA lambda not found");

        String newName = src.name + "$slm";
        MethodNode copy = cloneMethod(src);
        copy.name = newName;
        copy.access = Opcodes.ACC_PRIVATE | Opcodes.ACC_SYNTHETIC;
        for (AbstractInsnNode a : copy.instructions) {
            if (a instanceof FieldInsnNode f && f.getOpcode() == Opcodes.GETSTATIC
                    && f.owner.equals(TT) && f.name.equals("ELYTRA")) {
                f.name = NEW_NAME;
            }
        }
        cn.methods.add(copy);

        // 克隆 invokedynamic（拿 ELYTRA 按钮的那个）
        InvokeDynamicInsnNode srcIndy = null;
        for (AbstractInsnNode a : ins) {
            if (a instanceof InvokeDynamicInsnNode d && d.bsmArgs.length >= 2
                    && d.bsmArgs[1] instanceof Handle h && h.getName().equals(src.name)) {
                srcIndy = d;
                break;
            }
        }
        if (srcIndy == null) throw new IllegalStateException("indy for ELYTRA lambda not found");

        Object[] bsmArgs = srcIndy.bsmArgs.clone();
        Handle srcHandle = (Handle) srcIndy.bsmArgs[1];
        bsmArgs[1] = new Handle(srcHandle.getTag(), cn.name, newName, src.desc, srcHandle.isInterface());
        InvokeDynamicInsnNode newIndy = new InvokeDynamicInsnNode(srcIndy.name, srcIndy.desc, srcIndy.bsm, bsmArgs);

        // 插到 PUTFIELD entry 之前
        FieldInsnNode putEntry = null;
        for (AbstractInsnNode a : ins) {
            if (a instanceof FieldInsnNode f && f.getOpcode() == Opcodes.PUTFIELD && f.name.equals("entry")) {
                putEntry = f;
            }
        }
        if (putEntry == null) throw new IllegalStateException("PUTFIELD entry not found");

        InsnList add = new InsnList();
        add.add(new InsnNode(Opcodes.DUP));
        add.add(new IntInsnNode(Opcodes.BIPUSH, 5));
        add.add(new TypeInsnNode(Opcodes.NEW, "dev/rstminecraft/RSTAbstractScr$SrcButtonEntry"));
        add.add(new InsnNode(Opcodes.DUP));
        add.add(new LdcInsnNode("开始飞行(SLM甲飞接管)"));
        add.add(new LdcInsnNode("用 SlimefunHelper 甲飞驱动 baritone：不穿鞘翅、不掉耐久"));
        add.add(new VarInsnNode(Opcodes.ALOAD, 0));   // lambda 捕获 this
        add.add(newIndy);
        add.add(new MethodInsnNode(Opcodes.INVOKESPECIAL, "dev/rstminecraft/RSTAbstractScr$SrcButtonEntry",
                "<init>", "(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Runnable;)V", false));
        add.add(new InsnNode(Opcodes.AASTORE));
        ins.insertBefore(putEntry, add);
        System.out.println("gui: added 4th button using lambda " + src.name + " -> " + newName);
    }
}
