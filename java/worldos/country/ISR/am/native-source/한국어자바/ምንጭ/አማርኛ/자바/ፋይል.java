// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package አማርኛ.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 ፋይል 도우미. */
public final class ፋይል {
    private ፋይል() {}
    public static Path መተላለፊያ(String ስም) { return Path.of(ስም); }
    public static String ማንበቢያ(Path መተላለፊያ) throws IOException {
        return Files.readString(መተላለፊያ, StandardCharsets.UTF_8);
    }
    public static Path መጻፊያ(Path መተላለፊያ, String ይዘት_እሴት) throws IOException {
        return Files.writeString(መተላለፊያ, ይዘት_እሴት, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path መተላለፊያ) throws IOException { return Files.readAllBytes(መተላለፊያ); }
    public static Path ጻፍ_ባይት_እሴት(Path መተላለፊያ, byte[] ይዘት_እሴት) throws IOException { return Files.write(መተላለፊያ, ይዘት_እሴት); }
    public static Path ፍጠር_ማውጫ(Path መተላለፊያ) throws IOException { return Files.createDirectories(መተላለፊያ); }
    public static boolean 있는가(Path መተላለፊያ) { return Files.exists(መተላለፊያ); }
    public static boolean አስወግድ_ምዝግብ_c8dbc399(Path መተላለፊያ) throws IOException { return Files.deleteIfExists(መተላለፊያ); }
    public static List<Path> ምዝግብ_ዝርዝር(Path መተላለፊያ) throws IOException {
        try (Stream<Path> ምዝግብ_እሴት = Files.list(መተላለፊያ)) { return ምዝግብ_እሴት.sorted().collect(Collectors.toList()); }
    }
}
