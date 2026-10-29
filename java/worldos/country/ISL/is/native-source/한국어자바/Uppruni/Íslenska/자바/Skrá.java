// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Íslenska.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 Skrá 도우미. */
public final class Skrá {
    private Skrá() {}
    public static Path SLÓÐ(String Heiti) { return Path.of(Heiti); }
    public static String Lestur(Path SLÓÐ) throws IOException {
        return Files.readString(SLÓÐ, StandardCharsets.UTF_8);
    }
    public static Path Skrift(Path SLÓÐ, String Efni_VALUE) throws IOException {
        return Files.writeString(SLÓÐ, Efni_VALUE, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path SLÓÐ) throws IOException { return Files.readAllBytes(SLÓÐ); }
    public static Path skrifa_bæti_VALUE(Path SLÓÐ, byte[] Efni_VALUE) throws IOException { return Files.write(SLÓÐ, Efni_VALUE); }
    public static Path stofna_skráasafn(Path SLÓÐ) throws IOException { return Files.createDirectories(SLÓÐ); }
    public static boolean 있는가(Path SLÓÐ) { return Files.exists(SLÓÐ); }
    public static boolean eyða_færsla(Path SLÓÐ) throws IOException { return Files.deleteIfExists(SLÓÐ); }
    public static List<Path> færsla_Listi(Path SLÓÐ) throws IOException {
        try (Stream<Path> færsla_VALUE = Files.list(SLÓÐ)) { return færsla_VALUE.sorted().collect(Collectors.toList()); }
    }
}
