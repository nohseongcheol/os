// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 Датотека 도우미. */
public final class Датотека {
    private Датотека() {}
    public static Path ПУТАЊА(String Назив) { return Path.of(Назив); }
    public static String Чита(Path ПУТАЊА) throws IOException {
        return Files.readString(ПУТАЊА, StandardCharsets.UTF_8);
    }
    public static Path Пише(Path ПУТАЊА, String 내용) throws IOException {
        return Files.writeString(ПУТАЊА, 내용, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path ПУТАЊА) throws IOException { return Files.readAllBytes(ПУТАЊА); }
    public static Path 바이트쓰기(Path ПУТАЊА, byte[] 내용) throws IOException { return Files.write(ПУТАЊА, 내용); }
    public static Path 폴더만들기(Path ПУТАЊА) throws IOException { return Files.createDirectories(ПУТАЊА); }
    public static boolean 있는가(Path ПУТАЊА) { return Files.exists(ПУТАЊА); }
    public static boolean 지우기(Path ПУТАЊА) throws IOException { return Files.deleteIfExists(ПУТАЊА); }
    public static List<Path> 목록(Path ПУТАЊА) throws IOException {
        try (Stream<Path> 항목 = Files.list(ПУТАЊА)) { return 항목.sorted().collect(Collectors.toList()); }
    }
}
