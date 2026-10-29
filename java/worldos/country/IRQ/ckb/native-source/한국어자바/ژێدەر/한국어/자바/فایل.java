// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 فایل 도우미. */
public final class فایل {
    private فایل() {}
    public static Path گوزەر(String ناو) { return Path.of(ناو); }
    public static String 읽기(Path گوزەر) throws IOException {
        return Files.readString(گوزەر, StandardCharsets.UTF_8);
    }
    public static Path ڕایت_کردن(Path گوزەر, String ناوەرۆک_نرخ) throws IOException {
        return Files.writeString(گوزەر, ناوەرۆک_نرخ, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path گوزەر) throws IOException { return Files.readAllBytes(گوزەر); }
    public static Path ڕایت_کردن_بایت_نرخ(Path گوزەر, byte[] ناوەرۆک_نرخ) throws IOException { return Files.write(گوزەر, ناوەرۆک_نرخ); }
    public static Path دروستکردن_ڕێبەرنامە(Path گوزەر) throws IOException { return Files.createDirectories(گوزەر); }
    public static boolean 있는가(Path گوزەر) { return Files.exists(گوزەر); }
    public static boolean 지우기(Path گوزەر) throws IOException { return Files.deleteIfExists(گوزەر); }
    public static List<Path> تێنووسین_لیست(Path گوزەر) throws IOException {
        try (Stream<Path> تێنووسین_نرخ = Files.list(گوزەر)) { return تێنووسین_نرخ.sorted().collect(Collectors.toList()); }
    }
}
