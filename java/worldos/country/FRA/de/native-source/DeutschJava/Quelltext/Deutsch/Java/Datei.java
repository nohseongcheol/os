// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.Java;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** UTF-8-Dateihilfe, die standardmäßige Path und IOException unmittelbar verwendet. */
public final class Datei {
    private Datei() {}
    public static Path pfad(String Name) { return Path.of(Name); }
    public static String lesen(Path pfad) throws IOException {
        return Files.readString(pfad, StandardCharsets.UTF_8);
    }
    public static Path schreiben(Path pfad, String inhaltswertWert) throws IOException {
        return Files.writeString(pfad, inhaltswertWert, StandardCharsets.UTF_8);
    }
    public static byte[] byteWertLesen(Path pfad) throws IOException { return Files.readAllBytes(pfad); }
    public static Path byteWertSchreiben(Path pfad, byte[] inhaltswertWert) throws IOException { return Files.write(pfad, inhaltswertWert); }
    public static Path verzeichnisErstellen(Path pfad) throws IOException { return Files.createDirectories(pfad); }
    public static boolean führtAusVorhanden(Path pfad) { return Files.exists(pfad); }
    public static boolean eintragTilgen(Path pfad) throws IOException { return Files.deleteIfExists(pfad); }
    public static List<Path> eintragListe(Path pfad) throws IOException {
        try (Stream<Path> eintragWert = Files.list(pfad)) { return eintragWert.sorted().collect(Collectors.toList()); }
    }
}
