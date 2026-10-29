// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Isi_Zulu.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 Ihele 도우미. */
public final class Ihele {
    private Ihele() {}
    public static Path Indlela_2(String Igama) { return Path.of(Igama); }
    public static String Funda(Path Indlela_2) throws IOException {
        return Files.readString(Indlela_2, StandardCharsets.UTF_8);
    }
    public static Path Bhala(Path Indlela_2, String Okuqukethwe_inani) throws IOException {
        return Files.writeString(Indlela_2, Okuqukethwe_inani, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path Indlela_2) throws IOException { return Files.readAllBytes(Indlela_2); }
    public static Path bhala_ibhayithi_inani(Path Indlela_2, byte[] Okuqukethwe_inani) throws IOException { return Files.write(Indlela_2, Okuqukethwe_inani); }
    public static Path yakha_umkhombandlela(Path Indlela_2) throws IOException { return Files.createDirectories(Indlela_2); }
    public static boolean 있는가(Path Indlela_2) { return Files.exists(Indlela_2); }
    public static boolean 지우기(Path Indlela_2) throws IOException { return Files.deleteIfExists(Indlela_2); }
    public static List<Path> okufakwayo_Uhlu(Path Indlela_2) throws IOException {
        try (Stream<Path> okufakwayo_inani = Files.list(Indlela_2)) { return okufakwayo_inani.sorted().collect(Collectors.toList()); }
    }
}
