// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package hrvatski.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 Datoteka 도우미. */
public final class Datoteka {
    private Datoteka() {}
    public static Path PUTANJA(String Ime) { return Path.of(Ime); }
    public static String Čitaj(Path PUTANJA) throws IOException {
        return Files.readString(PUTANJA, StandardCharsets.UTF_8);
    }
    public static Path Zapisuj(Path PUTANJA, String Sadržaj_VALUE) throws IOException {
        return Files.writeString(PUTANJA, Sadržaj_VALUE, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path PUTANJA) throws IOException { return Files.readAllBytes(PUTANJA); }
    public static Path zapisivanje_bajt_VALUE(Path PUTANJA, byte[] Sadržaj_VALUE) throws IOException { return Files.write(PUTANJA, Sadržaj_VALUE); }
    public static Path Create_imenik(Path PUTANJA) throws IOException { return Files.createDirectories(PUTANJA); }
    public static boolean 있는가(Path PUTANJA) { return Files.exists(PUTANJA); }
    public static boolean izbrisati_unos(Path PUTANJA) throws IOException { return Files.deleteIfExists(PUTANJA); }
    public static List<Path> unos_Popis(Path PUTANJA) throws IOException {
        try (Stream<Path> unos_VALUE = Files.list(PUTANJA)) { return unos_VALUE.sorted().collect(Collectors.toList()); }
    }
}
