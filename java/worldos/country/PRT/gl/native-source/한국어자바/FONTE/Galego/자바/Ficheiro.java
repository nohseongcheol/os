// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Galego.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 Ficheiro 도우미. */
public final class Ficheiro {
    private Ficheiro() {}
    public static Path CAMIÑO(String Nome) { return Path.of(Nome); }
    public static String Lectura(Path CAMIÑO) throws IOException {
        return Files.readString(CAMIÑO, StandardCharsets.UTF_8);
    }
    public static Path Escritura(Path CAMIÑO, String Contido_VALOR) throws IOException {
        return Files.writeString(CAMIÑO, Contido_VALOR, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path CAMIÑO) throws IOException { return Files.readAllBytes(CAMIÑO); }
    public static Path escribir_byte_VALOR(Path CAMIÑO, byte[] Contido_VALOR) throws IOException { return Files.write(CAMIÑO, Contido_VALOR); }
    public static Path crear_directorio(Path CAMIÑO) throws IOException { return Files.createDirectories(CAMIÑO); }
    public static boolean 있는가(Path CAMIÑO) { return Files.exists(CAMIÑO); }
    public static boolean borrar_introdución(Path CAMIÑO) throws IOException { return Files.deleteIfExists(CAMIÑO); }
    public static List<Path> introdución_Lista(Path CAMIÑO) throws IOException {
        try (Stream<Path> introdución_VALOR = Files.list(CAMIÑO)) { return introdución_VALOR.sorted().collect(Collectors.toList()); }
    }
}
