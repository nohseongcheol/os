// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 فائل 도우미. */
public final class فائل {
    private فائل() {}
    public static Path راههه(String نالو) { return Path.of(نالو); }
    public static String 읽기(Path راههه) throws IOException {
        return Files.readString(راههه, StandardCharsets.UTF_8);
    }
    public static Path لکو(Path راههه, String مواد_قدر) throws IOException {
        return Files.writeString(راههه, مواد_قدر, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path راههه) throws IOException { return Files.readAllBytes(راههه); }
    public static Path لکو_بائٽ_قدر(Path راههه, byte[] مواد_قدر) throws IOException { return Files.write(راههه, مواد_قدر); }
    public static Path ٺاھيو_ڊائريڪٽري(Path راههه) throws IOException { return Files.createDirectories(راههه); }
    public static boolean 있는가(Path راههه) { return Files.exists(راههه); }
    public static boolean 지우기(Path راههه) throws IOException { return Files.deleteIfExists(راههه); }
    public static List<Path> داخلا_فهرست(Path راههه) throws IOException {
        try (Stream<Path> داخلا_قدر = Files.list(راههه)) { return داخلا_قدر.sorted().collect(Collectors.toList()); }
    }
}
