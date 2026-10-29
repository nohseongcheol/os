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
    public static Path راہ(String ناں) { return Path.of(ناں); }
    public static String 읽기(Path راہ) throws IOException {
        return Files.readString(راہ, StandardCharsets.UTF_8);
    }
    public static Path لکھو(Path راہ, String اجزاء_قدر) throws IOException {
        return Files.writeString(راہ, اجزاء_قدر, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path راہ) throws IOException { return Files.readAllBytes(راہ); }
    public static Path لکھو_بائٹ_قدر(Path راہ, byte[] اجزاء_قدر) throws IOException { return Files.write(راہ, اجزاء_قدر); }
    public static Path بنڑاؤ_ڈائریکٹری(Path راہ) throws IOException { return Files.createDirectories(راہ); }
    public static boolean 있는가(Path راہ) { return Files.exists(راہ); }
    public static boolean 지우기(Path راہ) throws IOException { return Files.deleteIfExists(راہ); }
    public static List<Path> داخلہ_فرست(Path راہ) throws IOException {
        try (Stream<Path> داخلہ_قدر = Files.list(راہ)) { return داخلہ_قدر.sorted().collect(Collectors.toList()); }
    }
}
