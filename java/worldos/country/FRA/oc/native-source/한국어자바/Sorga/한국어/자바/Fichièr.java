// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 Fichièr 도우미. */
public final class Fichièr {
    private Fichièr() {}
    public static Path CAMIN(String Nom) { return Path.of(Nom); }
    public static String Lectura(Path CAMIN) throws IOException {
        return Files.readString(CAMIN, StandardCharsets.UTF_8);
    }
    public static Path Escritura(Path CAMIN, String 내용) throws IOException {
        return Files.writeString(CAMIN, 내용, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path CAMIN) throws IOException { return Files.readAllBytes(CAMIN); }
    public static Path 바이트쓰기(Path CAMIN, byte[] 내용) throws IOException { return Files.write(CAMIN, 내용); }
    public static Path 폴더만들기(Path CAMIN) throws IOException { return Files.createDirectories(CAMIN); }
    public static boolean 있는가(Path CAMIN) { return Files.exists(CAMIN); }
    public static boolean 지우기(Path CAMIN) throws IOException { return Files.deleteIfExists(CAMIN); }
    public static List<Path> 목록(Path CAMIN) throws IOException {
        try (Stream<Path> 항목 = Files.list(CAMIN)) { return 항목.sorted().collect(Collectors.toList()); }
    }
}
