// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ikinyarwanda.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 Idosiye 도우미. */
public final class Idosiye {
    private Idosiye() {}
    public static Path Inzira(String Izina) { return Path.of(Izina); }
    public static String 읽기(Path Inzira) throws IOException {
        return Files.readString(Inzira, StandardCharsets.UTF_8);
    }
    public static Path kwandika(Path Inzira, String Ibirimo_agaciro) throws IOException {
        return Files.writeString(Inzira, Ibirimo_agaciro, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path Inzira) throws IOException { return Files.readAllBytes(Inzira); }
    public static Path kwandika_bayiti_agaciro(Path Inzira, byte[] Ibirimo_agaciro) throws IOException { return Files.write(Inzira, Ibirimo_agaciro); }
    public static Path kurema_ububiko(Path Inzira) throws IOException { return Files.createDirectories(Inzira); }
    public static boolean 있는가(Path Inzira) { return Files.exists(Inzira); }
    public static boolean 지우기(Path Inzira) throws IOException { return Files.deleteIfExists(Inzira); }
    public static List<Path> icyinjizwa_Urutonde(Path Inzira) throws IOException {
        try (Stream<Path> icyinjizwa_agaciro = Files.list(Inzira)) { return icyinjizwa_agaciro.sorted().collect(Collectors.toList()); }
    }
}
