// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 Kartelë 도우미. */
public final class Kartelë {
    private Kartelë() {}
    public static Path POZICIONI(String Emër) { return Path.of(Emër); }
    public static String Leximi(Path POZICIONI) throws IOException {
        return Files.readString(POZICIONI, StandardCharsets.UTF_8);
    }
    public static Path Shkrimi(Path POZICIONI, String Përmbajtje_VALUE) throws IOException {
        return Files.writeString(POZICIONI, Përmbajtje_VALUE, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path POZICIONI) throws IOException { return Files.readAllBytes(POZICIONI); }
    public static Path shkruaj_bajt_VALUE(Path POZICIONI, byte[] Përmbajtje_VALUE) throws IOException { return Files.write(POZICIONI, Përmbajtje_VALUE); }
    public static Path Krijo_direktori(Path POZICIONI) throws IOException { return Files.createDirectories(POZICIONI); }
    public static boolean 있는가(Path POZICIONI) { return Files.exists(POZICIONI); }
    public static boolean spastroj_futje(Path POZICIONI) throws IOException { return Files.deleteIfExists(POZICIONI); }
    public static List<Path> futje_Listë(Path POZICIONI) throws IOException {
        try (Stream<Path> futje_VALUE = Files.list(POZICIONI)) { return futje_VALUE.sorted().collect(Collectors.toList()); }
    }
}
