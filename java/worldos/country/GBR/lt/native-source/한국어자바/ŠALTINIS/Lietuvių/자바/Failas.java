// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lietuvių.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 Failas 도우미. */
public final class Failas {
    private Failas() {}
    public static Path KELIAS(String Pavadinimas_2) { return Path.of(Pavadinimas_2); }
    public static String Skaitymas(Path KELIAS) throws IOException {
        return Files.readString(KELIAS, StandardCharsets.UTF_8);
    }
    public static Path Rašymas(Path KELIAS, String Turinys_VALUE) throws IOException {
        return Files.writeString(KELIAS, Turinys_VALUE, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path KELIAS) throws IOException { return Files.readAllBytes(KELIAS); }
    public static Path rašymas_baitas_VALUE(Path KELIAS, byte[] Turinys_VALUE) throws IOException { return Files.write(KELIAS, Turinys_VALUE); }
    public static Path kurti_Katalogas(Path KELIAS) throws IOException { return Files.createDirectories(KELIAS); }
    public static boolean 있는가(Path KELIAS) { return Files.exists(KELIAS); }
    public static boolean ištrinti_įrašas(Path KELIAS) throws IOException { return Files.deleteIfExists(KELIAS); }
    public static List<Path> įrašas_Sąrašas(Path KELIAS) throws IOException {
        try (Stream<Path> įrašas_VALUE = Files.list(KELIAS)) { return įrašas_VALUE.sorted().collect(Collectors.toList()); }
    }
}
