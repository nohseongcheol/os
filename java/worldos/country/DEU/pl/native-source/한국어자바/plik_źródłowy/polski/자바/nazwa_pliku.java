// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package polski.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 nazwa_pliku pomocnik_WARTOŚĆ. */
public final class nazwa_pliku {
    private nazwa_pliku() {}
    public static Path ścieżka_2(String Nazwa) { return Path.of(Nazwa); }
    public static String Odczyt(Path ścieżka_2) throws IOException {
        return Files.readString(ścieżka_2, StandardCharsets.UTF_8);
    }
    public static Path Zapis(Path ścieżka_2, String treść_WARTOŚĆ_cb0f2404) throws IOException {
        return Files.writeString(ścieżka_2, treść_WARTOŚĆ_cb0f2404, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path ścieżka_2) throws IOException { return Files.readAllBytes(ścieżka_2); }
    public static Path zapis_bajt_WARTOŚĆ(Path ścieżka_2, byte[] treść_WARTOŚĆ_cb0f2404) throws IOException { return Files.write(ścieżka_2, treść_WARTOŚĆ_cb0f2404); }
    public static Path Twórca_Katalog(Path ścieżka_2) throws IOException { return Files.createDirectories(ścieżka_2); }
    public static boolean 있는가(Path ścieżka_2) { return Files.exists(ścieżka_2); }
    public static boolean usunąć_wpis(Path ścieżka_2) throws IOException { return Files.deleteIfExists(ścieżka_2); }
    public static List<Path> wpis_Lista(Path ścieżka_2) throws IOException {
        try (Stream<Path> wpis_WARTOŚĆ = Files.list(ścieżka_2)) { return wpis_WARTOŚĆ.sorted().collect(Collectors.toList()); }
    }
}
