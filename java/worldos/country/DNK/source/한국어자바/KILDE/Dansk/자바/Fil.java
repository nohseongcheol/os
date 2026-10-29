// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Dansk.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 Fil hjælper_VÆRDI. */
public final class Fil {
    private Fil() {}
    public static Path Sti(String Navn) { return Path.of(Navn); }
    public static String Læse(Path Sti) throws IOException {
        return Files.readString(Sti, StandardCharsets.UTF_8);
    }
    public static Path Skrive(Path Sti, String Indhold_VÆRDI) throws IOException {
        return Files.writeString(Sti, Indhold_VÆRDI, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path Sti) throws IOException { return Files.readAllBytes(Sti); }
    public static Path skrive_byte_VÆRDI(Path Sti, byte[] Indhold_VÆRDI) throws IOException { return Files.write(Sti, Indhold_VÆRDI); }
    public static Path åbne_mappe(Path Sti) throws IOException { return Files.createDirectories(Sti); }
    public static boolean 있는가(Path Sti) { return Files.exists(Sti); }
    public static boolean slette_post(Path Sti) throws IOException { return Files.deleteIfExists(Sti); }
    public static List<Path> post_Liste(Path Sti) throws IOException {
        try (Stream<Path> post_VÆRDI_962f286b = Files.list(Sti)) { return post_VÆRDI_962f286b.sorted().collect(Collectors.toList()); }
    }
}
