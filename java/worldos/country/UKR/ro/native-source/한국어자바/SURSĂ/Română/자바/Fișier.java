// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Română.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 Fișier 도우미. */
public final class Fișier {
    private Fișier() {}
    public static Path Cale(String Nume) { return Path.of(Nume); }
    public static String Citire(Path Cale) throws IOException {
        return Files.readString(Cale, StandardCharsets.UTF_8);
    }
    public static Path Scriere(Path Cale, String Conținut_VALUE) throws IOException {
        return Files.writeString(Cale, Conținut_VALUE, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path Cale) throws IOException { return Files.readAllBytes(Cale); }
    public static Path scriere_byte_VALUE(Path Cale, byte[] Conținut_VALUE) throws IOException { return Files.write(Cale, Conținut_VALUE); }
    public static Path crea_Director(Path Cale) throws IOException { return Files.createDirectories(Cale); }
    public static boolean 있는가(Path Cale) { return Files.exists(Cale); }
    public static boolean șterge_intrare(Path Cale) throws IOException { return Files.deleteIfExists(Cale); }
    public static List<Path> intrare_Listă(Path Cale) throws IOException {
        try (Stream<Path> intrare_VALUE = Files.list(Cale)) { return intrare_VALUE.sorted().collect(Collectors.toList()); }
    }
}
