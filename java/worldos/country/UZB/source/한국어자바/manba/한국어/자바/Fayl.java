// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 Fayl 도우미. */
public final class Fayl {
    private Fayl() {}
    public static Path yo_l(String Nomi) { return Path.of(Nomi); }
    public static String Oʻqish(Path yo_l) throws IOException {
        return Files.readString(yo_l, StandardCharsets.UTF_8);
    }
    public static Path Yozish(Path yo_l, String tarkib_VALUE) throws IOException {
        return Files.writeString(yo_l, tarkib_VALUE, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path yo_l) throws IOException { return Files.readAllBytes(yo_l); }
    public static Path yozmoq_bayt_VALUE(Path yo_l, byte[] tarkib_VALUE) throws IOException { return Files.write(yo_l, tarkib_VALUE); }
    public static Path Yaratish_katalog(Path yo_l) throws IOException { return Files.createDirectories(yo_l); }
    public static boolean 있는가(Path yo_l) { return Files.exists(yo_l); }
    public static boolean tozalash_kiritish(Path yo_l) throws IOException { return Files.deleteIfExists(yo_l); }
    public static List<Path> kiritish_Ro_yxat(Path yo_l) throws IOException {
        try (Stream<Path> kiritish_VALUE = Files.list(yo_l)) { return kiritish_VALUE.sorted().collect(Collectors.toList()); }
    }
}
