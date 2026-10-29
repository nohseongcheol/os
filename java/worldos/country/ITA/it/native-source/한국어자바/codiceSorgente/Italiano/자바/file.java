// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Italiano.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 file helper_VALORE. */
public final class file {
    private file() {}
    public static Path percorso(String Nome) { return Path.of(Nome); }
    public static String Lettura(Path percorso) throws IOException {
        return Files.readString(percorso, StandardCharsets.UTF_8);
    }
    public static Path Scrittura(Path percorso, String Contenuto_VALORE) throws IOException {
        return Files.writeString(percorso, Contenuto_VALORE, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path percorso) throws IOException { return Files.readAllBytes(percorso); }
    public static Path scrivere_byte_VALORE(Path percorso, byte[] Contenuto_VALORE) throws IOException { return Files.write(percorso, Contenuto_VALORE); }
    public static Path Crea_elenco(Path percorso) throws IOException { return Files.createDirectories(percorso); }
    public static boolean 있는가(Path percorso) { return Files.exists(percorso); }
    public static boolean cancellare_voce(Path percorso) throws IOException { return Files.deleteIfExists(percorso); }
    public static List<Path> voce_elenco(Path percorso) throws IOException {
        try (Stream<Path> voce_VALORE = Files.list(percorso)) { return voce_VALORE.sorted().collect(Collectors.toList()); }
    }
}
