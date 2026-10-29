// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 Besjtandj 도우미. */
public final class Besjtandj {
    private Besjtandj() {}
    public static Path Paad(String Naam) { return Path.of(Naam); }
    public static String Laeze(Path Paad) throws IOException {
        return Files.readString(Paad, StandardCharsets.UTF_8);
    }
    public static Path Sjrieve(Path Paad, String 내용) throws IOException {
        return Files.writeString(Paad, 내용, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path Paad) throws IOException { return Files.readAllBytes(Paad); }
    public static Path 바이트쓰기(Path Paad, byte[] 내용) throws IOException { return Files.write(Paad, 내용); }
    public static Path 폴더만들기(Path Paad) throws IOException { return Files.createDirectories(Paad); }
    public static boolean 있는가(Path Paad) { return Files.exists(Paad); }
    public static boolean 지우기(Path Paad) throws IOException { return Files.deleteIfExists(Paad); }
    public static List<Path> 목록(Path Paad) throws IOException {
        try (Stream<Path> 항목 = Files.list(Paad)) { return 항목.sorted().collect(Collectors.toList()); }
    }
}
