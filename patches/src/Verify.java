import org.objectweb.asm.ClassReader;
import org.objectweb.asm.Opcodes;
import org.objectweb.asm.tree.*;
import org.objectweb.asm.tree.analysis.*;
import java.nio.file.*;

public class Verify {
    public static void main(String[] a) throws Exception {
        int bad = 0;
        for (String path : a) {
            ClassNode cn = new ClassNode();
            new ClassReader(Files.readAllBytes(Paths.get(path))).accept(cn, 0);
            for (MethodNode m : cn.methods) {
                if ((m.access & Opcodes.ACC_ABSTRACT) != 0 || m.instructions.size() == 0) continue;
                try {
                    Analyzer<BasicValue> an = new Analyzer<>(new BasicVerifier());
                    an.analyze(cn.name, m);
                    System.out.println("OK   " + cn.name + "." + m.name + m.desc);
                } catch (Throwable e) {
                    bad++;
                    System.out.println("FAIL " + cn.name + "." + m.name + m.desc + " -> " + e.getMessage());
                }
            }
        }
        System.out.println(bad == 0 ? "ALL OK" : ("FAILURES: " + bad));
    }
}
