// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 ھۆججەت 도우미. */
public final class ھۆججەت {
    private ھۆججەت() {}
    public static Path يول(String ئاتى) { return Path.of(ئاتى); }
    public static String ئوقۇ(Path يول) throws IOException {
        return Files.readString(يول, StandardCharsets.UTF_8);
    }
    public static Path ياز(Path يول, String مەزمۇن_قىممىتى) throws IOException {
        return Files.writeString(يول, مەزمۇن_قىممىتى, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path يول) throws IOException { return Files.readAllBytes(يول); }
    public static Path يازماق_بايت_قىممىتى(Path يول, byte[] مەزمۇن_قىممىتى) throws IOException { return Files.write(يول, مەزمۇن_قىممىتى); }
    public static Path قۇرۇش_مۇندەرىجە(Path يول) throws IOException { return Files.createDirectories(يول); }
    public static boolean 있는가(Path يول) { return Files.exists(يول); }
    public static boolean 지우기(Path يول) throws IOException { return Files.deleteIfExists(يول); }
    public static List<Path> كىرگۈزۈش_تىزىم(Path يول) throws IOException {
        try (Stream<Path> كىرگۈزۈش_قىممىتى = Files.list(يول)) { return كىرگۈزۈش_قىممىتى.sorted().collect(Collectors.toList()); }
    }
}
