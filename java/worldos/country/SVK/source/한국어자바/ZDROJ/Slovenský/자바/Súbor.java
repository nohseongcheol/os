// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovenský.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 Súbor 도우미. */
public final class Súbor {
    private Súbor() {}
    public static Path Cesta(String Názov) { return Path.of(Názov); }
    public static String Čítanie(Path Cesta) throws IOException {
        return Files.readString(Cesta, StandardCharsets.UTF_8);
    }
    public static Path Zápis(Path Cesta, String obsah_VALUE) throws IOException {
        return Files.writeString(Cesta, obsah_VALUE, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path Cesta) throws IOException { return Files.readAllBytes(Cesta); }
    public static Path zapísať_Byte_VALUE(Path Cesta, byte[] obsah_VALUE) throws IOException { return Files.write(Cesta, obsah_VALUE); }
    public static Path Create_Adresár(Path Cesta) throws IOException { return Files.createDirectories(Cesta); }
    public static boolean 있는가(Path Cesta) { return Files.exists(Cesta); }
    public static boolean vymazať_položka(Path Cesta) throws IOException { return Files.deleteIfExists(Cesta); }
    public static List<Path> položka_Zoznam(Path Cesta) throws IOException {
        try (Stream<Path> položka_VALUE = Files.list(Cesta)) { return položka_VALUE.sorted().collect(Collectors.toList()); }
    }
}
