// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Cymraeg.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 Ffeil 도우미. */
public final class Ffeil {
    private Ffeil() {}
    public static Path LLWYBR(String Enw) { return Path.of(Enw); }
    public static String Darllen(Path LLWYBR) throws IOException {
        return Files.readString(LLWYBR, StandardCharsets.UTF_8);
    }
    public static Path Ysgrifennu(Path LLWYBR, String Cynnwys_VALUE) throws IOException {
        return Files.writeString(LLWYBR, Cynnwys_VALUE, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path LLWYBR) throws IOException { return Files.readAllBytes(LLWYBR); }
    public static Path ysgrifennu_beit_VALUE(Path LLWYBR, byte[] Cynnwys_VALUE) throws IOException { return Files.write(LLWYBR, Cynnwys_VALUE); }
    public static Path Creu_cyfeiriadur(Path LLWYBR) throws IOException { return Files.createDirectories(LLWYBR); }
    public static boolean 있는가(Path LLWYBR) { return Files.exists(LLWYBR); }
    public static boolean 지우기(Path LLWYBR) throws IOException { return Files.deleteIfExists(LLWYBR); }
    public static List<Path> cofnod_Rhestr(Path LLWYBR) throws IOException {
        try (Stream<Path> cofnod_VALUE = Files.list(LLWYBR)) { return cofnod_VALUE.sorted().collect(Collectors.toList()); }
    }
}
