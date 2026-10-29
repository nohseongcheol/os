// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Euskara.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 Fitxategia 도우미. */
public final class Fitxategia {
    private Fitxategia() {}
    public static Path Bide_izena(String Izena) { return Path.of(Izena); }
    public static String Irakurri(Path Bide_izena) throws IOException {
        return Files.readString(Bide_izena, StandardCharsets.UTF_8);
    }
    public static Path Idatzi(Path Bide_izena, String eduki_balio) throws IOException {
        return Files.writeString(Bide_izena, eduki_balio, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path Bide_izena) throws IOException { return Files.readAllBytes(Bide_izena); }
    public static Path idatzi_byte_balio(Path Bide_izena, byte[] eduki_balio) throws IOException { return Files.write(Bide_izena, eduki_balio); }
    public static Path sortu_direktorio(Path Bide_izena) throws IOException { return Files.createDirectories(Bide_izena); }
    public static boolean 있는가(Path Bide_izena) { return Files.exists(Bide_izena); }
    public static boolean ezabatu_sarrera(Path Bide_izena) throws IOException { return Files.deleteIfExists(Bide_izena); }
    public static List<Path> sarrera_Zerrenda(Path Bide_izena) throws IOException {
        try (Stream<Path> sarrera_balio = Files.list(Bide_izena)) { return sarrera_balio.sorted().collect(Collectors.toList()); }
    }
}
