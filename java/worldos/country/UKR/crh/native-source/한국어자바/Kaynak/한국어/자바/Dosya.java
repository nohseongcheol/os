// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 Dosya 도우미. */
public final class Dosya {
    private Dosya() {}
    public static Path Yolçıq(String İsim) { return Path.of(İsim); }
    public static String Okuma(Path Yolçıq) throws IOException {
        return Files.readString(Yolçıq, StandardCharsets.UTF_8);
    }
    public static Path Yazma(Path Yolçıq, String 내용) throws IOException {
        return Files.writeString(Yolçıq, 내용, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path Yolçıq) throws IOException { return Files.readAllBytes(Yolçıq); }
    public static Path 바이트쓰기(Path Yolçıq, byte[] 내용) throws IOException { return Files.write(Yolçıq, 내용); }
    public static Path 폴더만들기(Path Yolçıq) throws IOException { return Files.createDirectories(Yolçıq); }
    public static boolean 있는가(Path Yolçıq) { return Files.exists(Yolçıq); }
    public static boolean 지우기(Path Yolçıq) throws IOException { return Files.deleteIfExists(Yolçıq); }
    public static List<Path> 목록(Path Yolçıq) throws IOException {
        try (Stream<Path> 항목 = Files.list(Yolçıq)) { return 항목.sorted().collect(Collectors.toList()); }
    }
}
