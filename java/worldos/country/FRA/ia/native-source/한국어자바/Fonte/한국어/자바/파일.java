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
    public static Path Percurso(String Nomine) { return Path.of(Nomine); }
    public static String Lege(Path Percurso) throws IOException {
        return Files.readString(Percurso, StandardCharsets.UTF_8);
    }
    public static Path Scribe(Path Percurso, String 내용) throws IOException {
        return Files.writeString(Percurso, 내용, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path Percurso) throws IOException { return Files.readAllBytes(Percurso); }
    public static Path 바이트쓰기(Path Percurso, byte[] 내용) throws IOException { return Files.write(Percurso, 내용); }
    public static Path 폴더만들기(Path Percurso) throws IOException { return Files.createDirectories(Percurso); }
    public static boolean 있는가(Path Percurso) { return Files.exists(Percurso); }
    public static boolean 지우기(Path Percurso) throws IOException { return Files.deleteIfExists(Percurso); }
    public static List<Path> 목록(Path Percurso) throws IOException {
        try (Stream<Path> 항목 = Files.list(Percurso)) { return 항목.sorted().collect(Collectors.toList()); }
    }
}
