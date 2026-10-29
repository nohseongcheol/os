// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 Dosiero 도우미. */
public final class Dosiero {
    private Dosiero() {}
    public static Path Vojo(String Nomo) { return Path.of(Nomo); }
    public static String Lego(Path Vojo) throws IOException {
        return Files.readString(Vojo, StandardCharsets.UTF_8);
    }
    public static Path Skribo(Path Vojo, String 내용) throws IOException {
        return Files.writeString(Vojo, 내용, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path Vojo) throws IOException { return Files.readAllBytes(Vojo); }
    public static Path 바이트쓰기(Path Vojo, byte[] 내용) throws IOException { return Files.write(Vojo, 내용); }
    public static Path 폴더만들기(Path Vojo) throws IOException { return Files.createDirectories(Vojo); }
    public static boolean 있는가(Path Vojo) { return Files.exists(Vojo); }
    public static boolean 지우기(Path Vojo) throws IOException { return Files.deleteIfExists(Vojo); }
    public static List<Path> 목록(Path Vojo) throws IOException {
        try (Stream<Path> 항목 = Files.list(Vojo)) { return 항목.sorted().collect(Collectors.toList()); }
    }
}
