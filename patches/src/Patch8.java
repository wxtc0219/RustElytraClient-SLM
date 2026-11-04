import org.objectweb.asm.ClassReader;
import org.objectweb.asm.ClassWriter;
import org.objectweb.asm.Opcodes;
import org.objectweb.asm.tree.*;

import java.nio.file.Files;
import java.nio.file.Paths;

/**
 * RustElytraTask.RepairElytra 改成：SLM 甲飞接管模式直接 return；
 * 其他三个模式保持原作者逻辑不变。
 */
public class Patch8 {
    public static void main(String[] args) throws Exception {
        ClassNode cn = new ClassNode();
        new ClassReader(Files.readAllBytes(Paths.get(args[0]))).accept(cn, 0);
        boolean done = false;
        for (MethodNode m : cn.methods) {
            if (!m.name.equals("RepairElytra")) {
                continue;
            }
            LabelNode skip = new LabelNode();
            InsnList pre = new InsnList();
            pre.add(new MethodInsnNode(Opcodes.INVOKESTATIC, "dev/rstminecraft/T", "isSlm", "()Z", false));
            pre.add(new JumpInsnNode(Opcodes.IFEQ, skip));
            pre.add(new InsnNode(Opcodes.RETURN));
            pre.add(skip);
            // 方法入口处：局部变量就是参数，栈为空，所以是 F_SAME
            pre.add(new FrameNode(Opcodes.F_SAME, 0, null, 0, null));
            m.instructions.insert(pre);
            done = true;
            System.out.println("patched RepairElytra " + m.desc);
        }
        if (!done) {
            throw new IllegalStateException("RepairElytra not found");
        }
        ClassWriter cw = new ClassWriter(ClassWriter.COMPUTE_MAXS);
        cn.accept(cw);
        Files.write(Paths.get(args[1]), cw.toByteArray());
        System.out.println("written " + args[1]);
    }
}
