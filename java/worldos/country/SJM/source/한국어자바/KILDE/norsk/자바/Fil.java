// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package norsk.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 Fil hjelper_VERDI. */
public final class Fil {
    private Fil() {}
    public static Path Sti(String Navn) { return Path.of(Navn); }
    public static String Les(Path Sti) throws IOException {
        return Files.readString(Sti, StandardCharsets.UTF_8);
    }
    public static Path Skriv(Path Sti, String Innhold_VERDI) throws IOException {
        return Files.writeString(Sti, Innhold_VERDI, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path Sti) throws IOException { return Files.readAllBytes(Sti); }
    public static Path skrive_byte_VERDI(Path Sti, byte[] Innhold_VERDI) throws IOException { return Files.write(Sti, Innhold_VERDI); }
    public static Path åpne_katalog(Path Sti) throws IOException { return Files.createDirectories(Sti); }
    public static boolean 있는가(Path Sti) { return Files.exists(Sti); }
    public static boolean slette_oppføring(Path Sti) throws IOException { return Files.deleteIfExists(Sti); }
    public static List<Path> oppføring_Liste(Path Sti) throws IOException {
        try (Stream<Path> oppføring_VERDI = Files.list(Sti)) { return oppføring_VERDI.sorted().collect(Collectors.toList()); }
    }
}
