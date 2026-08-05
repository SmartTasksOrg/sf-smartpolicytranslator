import cloud.smarttasks.spt.SptClient;
import java.nio.file.*;
import java.util.*;
import java.util.stream.*;

public class Demo {
    public static void main(String[] args) throws Exception {
        String ds = args[0], out = args[1];
        Files.createDirectories(Paths.get(out));
        String base = System.getenv().getOrDefault("SPT_URL", "http://localhost:8000");
        SptClient spt = new SptClient(base);
        List<Path> files = Files.list(Paths.get(ds))
            .filter(p -> p.toString().endsWith(".txt")).sorted().collect(Collectors.toList());
        for (Path f : files) {
            String text = Files.readString(f);
            String json = spt.translate(text, false, "lmstudio");
            String name = f.getFileName().toString().replaceAll("\\.txt$", "");
            Files.writeString(Paths.get(out, name + ".policy.json"), json);
            System.out.println("  " + name);
        }
    }
}
