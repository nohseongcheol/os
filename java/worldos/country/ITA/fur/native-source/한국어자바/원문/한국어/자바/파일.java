// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 파일 도우미. */
public final class 파일 {
    private 파일() {}
    public static Path Percors(String Nom) { return Path.of(Nom); }
    public static String Lei(Path Percors) throws IOException {
        return Files.readString(Percors, StandardCharsets.UTF_8);
    }
    public static Path Scrivi(Path Percors, String 내용) throws IOException {
        return Files.writeString(Percors, 내용, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path Percors) throws IOException { return Files.readAllBytes(Percors); }
    public static Path 바이트쓰기(Path Percors, byte[] 내용) throws IOException { return Files.write(Percors, 내용); }
    public static Path 폴더만들기(Path Percors) throws IOException { return Files.createDirectories(Percors); }
    public static boolean 있는가(Path Percors) { return Files.exists(Percors); }
    public static boolean 지우기(Path Percors) throws IOException { return Files.deleteIfExists(Percors); }
    public static List<Path> 목록(Path Percors) throws IOException {
        try (Stream<Path> 항목 = Files.list(Percors)) { return 항목.sorted().collect(Collectors.toList()); }
    }
}
