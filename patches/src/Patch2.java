import org.objectweb.asm.ClassReader;
import org.objectweb.asm.ClassVisitor;
import org.objectweb.asm.ClassWriter;
import org.objectweb.asm.MethodVisitor;
import org.objectweb.asm.Opcodes;

import java.nio.file.Files;
import java.nio.file.Paths;

/** 针对 RustElytraClient beta1.6 的 RustSupplyTask:
 *  - ContainerScreenChecker: String.equalsIgnoreCase -> dev.rstminecraft.T.eq (去§/包含匹配)
 *  - WaitForScreen: 循环次数 20 -> 120 tick
 */
public class Patch2 {
    public static void main(String[] args) throws Exception {
        byte[] cls = Files.readAllBytes(Paths.get(args[0]));
        ClassReader cr = new ClassReader(cls);
        ClassWriter cw = new ClassWriter(cr, 0);
        ClassVisitor cv = new ClassVisitor(Opcodes.ASM9, cw) {
            @Override
            public MethodVisitor visitMethod(int access, String name, String desc, String sig, String[] ex) {
                MethodVisitor mv = super.visitMethod(access, name, desc, sig, ex);
                if (name.equals("WaitForScreen")) {
                    return new MethodVisitor(Opcodes.ASM9, mv) {
                        @Override
                        public void visitIntInsn(int opcode, int operand) {
                            if (opcode == Opcodes.BIPUSH && operand == 20) {
                                operand = 120;
                            }
                            super.visitIntInsn(opcode, operand);
                        }
                    };
                }
                if (name.equals("ContainerScreenChecker")) {
                    return new MethodVisitor(Opcodes.ASM9, mv) {
                        @Override
                        public void visitMethodInsn(int op, String owner, String nm, String d, boolean itf) {
                            if (op == Opcodes.INVOKEVIRTUAL
                                    && owner.equals("java/lang/String")
                                    && nm.equals("equalsIgnoreCase")
                                    && d.equals("(Ljava/lang/String;)Z")) {
                                super.visitMethodInsn(Opcodes.INVOKESTATIC, "dev/rstminecraft/T", "eq",
                                        "(Ljava/lang/String;Ljava/lang/String;)Z", false);
                                return;
                            }
                            super.visitMethodInsn(op, owner, nm, d, itf);
                        }
                    };
                }
                return mv;
            }
        };
        cr.accept(cv, 0);
        Files.write(Paths.get(args[1]), cw.toByteArray());
        System.out.println("patched -> " + args[1]);
    }
}
