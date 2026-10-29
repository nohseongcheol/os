// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 Fil 도우미. */
public final class Fil {
    private Fil() {}
    public static Path STIGE(String Namn) { return Path.of(Namn); }
    public static String Les(Path STIGE) throws IOException {
        return Files.readString(STIGE, StandardCharsets.UTF_8);
    }
    public static Path Skriv(Path STIGE, String Innhald_VALUE) throws IOException {
        return Files.writeString(STIGE, Innhald_VALUE, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path STIGE) throws IOException { return Files.readAllBytes(STIGE); }
    public static Path skrive_byte_VALUE(Path STIGE, byte[] Innhald_VALUE) throws IOException { return Files.write(STIGE, Innhald_VALUE); }
    public static Path Opprett_katalog(Path STIGE) throws IOException { return Files.createDirectories(STIGE); }
    public static boolean 있는가(Path STIGE) { return Files.exists(STIGE); }
    public static boolean 지우기(Path STIGE) throws IOException { return Files.deleteIfExists(STIGE); }
    public static List<Path> oppføring_Liste(Path STIGE) throws IOException {
        try (Stream<Path> oppføring_VALUE = Files.list(STIGE)) { return oppføring_VALUE.sorted().collect(Collectors.toList()); }
    }
}
