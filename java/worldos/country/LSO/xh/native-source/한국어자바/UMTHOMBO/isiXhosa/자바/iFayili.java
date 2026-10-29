// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package isiXhosa.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 iFayili 도우미. */
public final class iFayili {
    private iFayili() {}
    public static Path INDLELA(String Igama) { return Path.of(Igama); }
    public static String Funda(Path INDLELA) throws IOException {
        return Files.readString(INDLELA, StandardCharsets.UTF_8);
    }
    public static Path Bhala(Path INDLELA, String Isiqulatho_ixabiso) throws IOException {
        return Files.writeString(INDLELA, Isiqulatho_ixabiso, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path INDLELA) throws IOException { return Files.readAllBytes(INDLELA); }
    public static Path bhala_ibhayithi_ixabiso(Path INDLELA, byte[] Isiqulatho_ixabiso) throws IOException { return Files.write(INDLELA, Isiqulatho_ixabiso); }
    public static Path yila_isalathisi(Path INDLELA) throws IOException { return Files.createDirectories(INDLELA); }
    public static boolean 있는가(Path INDLELA) { return Files.exists(INDLELA); }
    public static boolean 지우기(Path INDLELA) throws IOException { return Files.deleteIfExists(INDLELA); }
    public static List<Path> ufako_nkcukacha_uludwe(Path INDLELA) throws IOException {
        try (Stream<Path> ufako_nkcukacha_ixabiso = Files.list(INDLELA)) { return ufako_nkcukacha_ixabiso.sorted().collect(Collectors.toList()); }
    }
}
