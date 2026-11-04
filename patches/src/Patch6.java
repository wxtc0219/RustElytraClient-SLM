import org.objectweb.asm.ClassReader;
import org.objectweb.asm.ClassWriter;
import org.objectweb.asm.Opcodes;
import org.objectweb.asm.tree.*;
import java.nio.file.*;

public class Patch6 {
    public static void main(String[] a) throws Exception {
        ClassNode cn = new ClassNode();
        new ClassReader(Files.readAllBytes(Paths.get(a[0]))).accept(cn, 0);
        MethodNode v = null;
        for (MethodNode m : cn.methods) if (m.name.equals("$values")) v = m;
        if (v == null) throw new IllegalStateException("no $values");
        InsnList ins = v.instructions;
        AbstractInsnNode ret = null;
        for (AbstractInsnNode n : ins) if (n.getOpcode() == Opcodes.ARETURN) ret = n;
        // 删掉 areturn 之后的所有真实指令
        boolean after = false;
        java.util.List<AbstractInsnNode> del = new java.util.ArrayList<>();
        for (AbstractInsnNode n : ins) {
            if (n == ret) { after = true; continue; }
            if (after && n.getOpcode() != -1) del.add(n);
        }
        for (AbstractInsnNode n : del) ins.remove(n);
        InsnList add = new InsnList();
        add.add(new InsnNode(Opcodes.DUP));
        add.add(new InsnNode(Opcodes.ICONST_3));
        add.add(new FieldInsnNode(Opcodes.GETSTATIC, "dev/rstminecraft/TaskThread$TaskType", "SLM_TAKEOVER", "Ldev/rstminecraft/TaskThread$TaskType;"));
        add.add(new InsnNode(Opcodes.AASTORE));
        ins.insertBefore(ret, add);
        ClassWriter cw = new ClassWriter(ClassWriter.COMPUTE_MAXS);
        cn.accept(cw);
        Files.write(Paths.get(a[1]), cw.toByteArray());
        System.out.println("ok, deleted " + del.size());
    }
}
