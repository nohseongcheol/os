// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 Restr 도우미. */
public final class Restr {
    private Restr() {}
    public static Path TREUG(String Anv) { return Path.of(Anv); }
    public static String Lenn(Path TREUG) throws IOException {
        return Files.readString(TREUG, StandardCharsets.UTF_8);
    }
    public static Path Skrivañ(Path TREUG, String 내용) throws IOException {
        return Files.writeString(TREUG, 내용, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path TREUG) throws IOException { return Files.readAllBytes(TREUG); }
    public static Path 바이트쓰기(Path TREUG, byte[] 내용) throws IOException { return Files.write(TREUG, 내용); }
    public static Path 폴더만들기(Path TREUG) throws IOException { return Files.createDirectories(TREUG); }
    public static boolean 있는가(Path TREUG) { return Files.exists(TREUG); }
    public static boolean 지우기(Path TREUG) throws IOException { return Files.deleteIfExists(TREUG); }
    public static List<Path> 목록(Path TREUG) throws IOException {
        try (Stream<Path> 항목 = Files.list(TREUG)) { return 항목.sorted().collect(Collectors.toList()); }
    }
}
