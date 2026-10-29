// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 Rakitra 도우미. */
public final class Rakitra {
    private Rakitra() {}
    public static Path LALANA(String Anarana) { return Path.of(Anarana); }
    public static String Mamaky(Path LALANA) throws IOException {
        return Files.readString(LALANA, StandardCharsets.UTF_8);
    }
    public static Path Manoratra(Path LALANA, String 내용) throws IOException {
        return Files.writeString(LALANA, 내용, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path LALANA) throws IOException { return Files.readAllBytes(LALANA); }
    public static Path 바이트쓰기(Path LALANA, byte[] 내용) throws IOException { return Files.write(LALANA, 내용); }
    public static Path 폴더만들기(Path LALANA) throws IOException { return Files.createDirectories(LALANA); }
    public static boolean 있는가(Path LALANA) { return Files.exists(LALANA); }
    public static boolean 지우기(Path LALANA) throws IOException { return Files.deleteIfExists(LALANA); }
    public static List<Path> 목록(Path LALANA) throws IOException {
        try (Stream<Path> 항목 = Files.list(LALANA)) { return 항목.sorted().collect(Collectors.toList()); }
    }
}
