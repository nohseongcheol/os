// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 Fajl 도우미. */
public final class Fajl {
    private Fajl() {}
    public static Path Putanja(String Naziv) { return Path.of(Naziv); }
    public static String Čitaj(Path Putanja) throws IOException {
        return Files.readString(Putanja, StandardCharsets.UTF_8);
    }
    public static Path Piši(Path Putanja, String Sadržaj_VALUE) throws IOException {
        return Files.writeString(Putanja, Sadržaj_VALUE, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path Putanja) throws IOException { return Files.readAllBytes(Putanja); }
    public static Path pisati_bajt_VALUE(Path Putanja, byte[] Sadržaj_VALUE) throws IOException { return Files.write(Putanja, Sadržaj_VALUE); }
    public static Path Create_Direktorij(Path Putanja) throws IOException { return Files.createDirectories(Putanja); }
    public static boolean 있는가(Path Putanja) { return Files.exists(Putanja); }
    public static boolean 지우기(Path Putanja) throws IOException { return Files.deleteIfExists(Putanja); }
    public static List<Path> unos_spisak(Path Putanja) throws IOException {
        try (Stream<Path> unos_VALUE = Files.list(Putanja)) { return unos_VALUE.sorted().collect(Collectors.toList()); }
    }
}
