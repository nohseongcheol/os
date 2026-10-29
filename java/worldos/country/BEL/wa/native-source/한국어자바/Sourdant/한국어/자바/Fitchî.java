// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 Fitchî 도우미. */
public final class Fitchî {
    private Fitchî() {}
    public static Path Tchimin(String No) { return Path.of(No); }
    public static String Lére(Path Tchimin) throws IOException {
        return Files.readString(Tchimin, StandardCharsets.UTF_8);
    }
    public static Path Sicrire(Path Tchimin, String 내용) throws IOException {
        return Files.writeString(Tchimin, 내용, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path Tchimin) throws IOException { return Files.readAllBytes(Tchimin); }
    public static Path 바이트쓰기(Path Tchimin, byte[] 내용) throws IOException { return Files.write(Tchimin, 내용); }
    public static Path 폴더만들기(Path Tchimin) throws IOException { return Files.createDirectories(Tchimin); }
    public static boolean 있는가(Path Tchimin) { return Files.exists(Tchimin); }
    public static boolean 지우기(Path Tchimin) throws IOException { return Files.deleteIfExists(Tchimin); }
    public static List<Path> 목록(Path Tchimin) throws IOException {
        try (Stream<Path> 항목 = Files.list(Tchimin)) { return 항목.sorted().collect(Collectors.toList()); }
    }
}
