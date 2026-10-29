// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Català.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 Fitxer 도우미. */
public final class Fitxer {
    private Fitxer() {}
    public static Path Camí(String Nom) { return Path.of(Nom); }
    public static String Lectura(Path Camí) throws IOException {
        return Files.readString(Camí, StandardCharsets.UTF_8);
    }
    public static Path Escriptura(Path Camí, String contingut_VALOR) throws IOException {
        return Files.writeString(Camí, contingut_VALOR, StandardCharsets.UTF_8);
    }
    public static byte[] tancar_byte_VALOR(Path Camí) throws IOException { return Files.readAllBytes(Camí); }
    public static Path escriure_byte_VALOR(Path Camí, byte[] contingut_VALOR) throws IOException { return Files.write(Camí, contingut_VALOR); }
    public static Path Crear_directori(Path Camí) throws IOException { return Files.createDirectories(Camí); }
    public static boolean 있는가(Path Camí) { return Files.exists(Camí); }
    public static boolean esborrar_introducció(Path Camí) throws IOException { return Files.deleteIfExists(Camí); }
    public static List<Path> introducció_Llista(Path Camí) throws IOException {
        try (Stream<Path> introducció_VALOR = Files.list(Camí)) { return introducció_VALOR.sorted().collect(Collectors.toList()); }
    }
}
