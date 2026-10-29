// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 Ficheru 도우미. */
public final class Ficheru {
    private Ficheru() {}
    public static Path Camín(String Nome) { return Path.of(Nome); }
    public static String Llectura(Path Camín) throws IOException {
        return Files.readString(Camín, StandardCharsets.UTF_8);
    }
    public static Path Escritura(Path Camín, String 내용) throws IOException {
        return Files.writeString(Camín, 내용, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path Camín) throws IOException { return Files.readAllBytes(Camín); }
    public static Path 바이트쓰기(Path Camín, byte[] 내용) throws IOException { return Files.write(Camín, 내용); }
    public static Path 폴더만들기(Path Camín) throws IOException { return Files.createDirectories(Camín); }
    public static boolean 있는가(Path Camín) { return Files.exists(Camín); }
    public static boolean 지우기(Path Camín) throws IOException { return Files.deleteIfExists(Camín); }
    public static List<Path> 목록(Path Camín) throws IOException {
        try (Stream<Path> 항목 = Files.list(Camín)) { return 항목.sorted().collect(Collectors.toList()); }
    }
}
