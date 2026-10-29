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
    public static Path Пише(Path ПУТАЊА, String Садржај_вриједност) throws IOException {
        return Files.writeString(ПУТАЊА, Садржај_вриједност, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path ПУТАЊА) throws IOException { return Files.readAllBytes(ПУТАЊА); }
    public static Path писати_бајт_вриједност(Path ПУТАЊА, byte[] Садржај_вриједност) throws IOException { return Files.write(ПУТАЊА, Садржај_вриједност); }
    public static Path Направи_именик(Path ПУТАЊА) throws IOException { return Files.createDirectories(ПУТАЊА); }
    public static boolean 있는가(Path ПУТАЊА) { return Files.exists(ПУТАЊА); }
    public static boolean 지우기(Path ПУТАЊА) throws IOException { return Files.deleteIfExists(ПУТАЊА); }
    public static List<Path> унос_Листа(Path ПУТАЊА) throws IOException {
        try (Stream<Path> унос_вриједност = Files.list(ПУТАЊА)) { return унос_вриједност.sorted().collect(Collectors.toList()); }
    }
}
