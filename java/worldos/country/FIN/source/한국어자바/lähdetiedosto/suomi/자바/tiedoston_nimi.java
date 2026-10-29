// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package suomi.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 tiedoston_nimi apuosa_ARVO. */
public final class tiedoston_nimi {
    private tiedoston_nimi() {}
    public static Path polku_2(String Nimi) { return Path.of(Nimi); }
    public static String Luku(Path polku_2) throws IOException {
        return Files.readString(polku_2, StandardCharsets.UTF_8);
    }
    public static Path Kirjoitus(Path polku_2, String Sisältö_ARVO) throws IOException {
        return Files.writeString(polku_2, Sisältö_ARVO, StandardCharsets.UTF_8);
    }
    public static byte[] lukea_tavu_ARVO(Path polku_2) throws IOException { return Files.readAllBytes(polku_2); }
    public static Path kirjoitus_tavu_ARVO(Path polku_2, byte[] Sisältö_ARVO) throws IOException { return Files.write(polku_2, Sisältö_ARVO); }
    public static Path Luo_Directory(Path polku_2) throws IOException { return Files.createDirectories(polku_2); }
    public static boolean 있는가(Path polku_2) { return Files.exists(polku_2); }
    public static boolean poistaa_merkintä_c8dbc399(Path polku_2) throws IOException { return Files.deleteIfExists(polku_2); }
    public static List<Path> merkintä_luettelo(Path polku_2) throws IOException {
        try (Stream<Path> merkintä_ARVO_962f286b = Files.list(polku_2)) { return merkintä_ARVO_962f286b.sorted().collect(Collectors.toList()); }
    }
}
