import org.objectweb.asm.ClassReader;
import org.objectweb.asm.ClassWriter;
import org.objectweb.asm.Opcodes;
import org.objectweb.asm.tree.*;

import java.nio.file.Files;
import java.nio.file.Paths;

/**
 * RustSupplyTask 里 "需要穿戴 耐久3 经验修补鞘翅" 的判断：
 * 保留原 boolean 值，但改成调用 T.elytraOk(boolean)：
 *   - 其它模式：wornOk 为真才通过（原版行为）
 *   - SLM 甲飞接管：背包里有鞘翅即可
 */
public class Patch7b {
    public static void main(String[] args) throws Exception {
        ClassNode cn = new ClassNode();
        new ClassReader(Files.readAllBytes(Paths.get(args[0]))).accept(cn, 0);
        int patched = 0;
        for (MethodNode m : cn.methods) {
            InsnList ins = m.instructions;
            for (AbstractInsnNode a : ins) {
                if (!(a instanceof LdcInsnNode ldc) || !(ldc.cst instanceof String s) || !s.contains("需要穿戴")) {
                    continue;
                }
                AbstractInsnNode n = a.getPrevious();
                AbstractInsnNode newExc = null;
                for (int k = 0; k < 12 && n != null; k++, n = n.getPrevious()) {
                    if (n instanceof TypeInsnNode t && t.getOpcode() == Opcodes.NEW && t.desc.contains("TaskException")) {
                        newExc = n;
                        break;
                    }
                }
                if (newExc == null) {
                    continue;
                }
                AbstractInsnNode jump = newExc.getPrevious();
                if (jump instanceof LabelNode) {
                    jump = jump.getPrevious();
                }
                if (!(jump instanceof JumpInsnNode jn)) {
                    continue;
                }
                // 在跳转前插入 T.elytraOk(Z)Z，把原来的 boolean 值当参数
                InsnList add = new InsnList();
                add.add(new MethodInsnNode(Opcodes.INVOKESTATIC, "dev/rstminecraft/T", "elytraOk", "(Z)Z", false));
                ins.insertBefore(jump, add);
                patched++;
                System.out.println("patched guard in " + m.name + m.desc);
            }
        }
        if (patched == 0) {
            throw new IllegalStateException("no guard patched");
        }
        ClassWriter cw = new ClassWriter(ClassWriter.COMPUTE_MAXS);
        cn.accept(cw);
        Files.write(Paths.get(args[1]), cw.toByteArray());
        System.out.println("done patched=" + patched);
    }
}
