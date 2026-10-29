// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Português.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 ficheiro auxiliar_VALOR. */
public final class ficheiro {
    private ficheiro() {}
    public static Path caminho(String Nome) { return Path.of(Nome); }
    public static String Leitura(Path caminho) throws IOException {
        return Files.readString(caminho, StandardCharsets.UTF_8);
    }
    public static Path Escrita(Path caminho, String Conteúdo_VALOR) throws IOException {
        return Files.writeString(caminho, Conteúdo_VALOR, StandardCharsets.UTF_8);
    }
    public static byte[] leitura_byte_VALOR(Path caminho) throws IOException { return Files.readAllBytes(caminho); }
    public static Path gravar_byte_VALOR(Path caminho, byte[] Conteúdo_VALOR) throws IOException { return Files.write(caminho, Conteúdo_VALOR); }
    public static Path Criar_Diretório(Path caminho) throws IOException { return Files.createDirectories(caminho); }
    public static boolean 있는가(Path caminho) { return Files.exists(caminho); }
    public static boolean apagar_entrada(Path caminho) throws IOException { return Files.deleteIfExists(caminho); }
    public static List<Path> entrada_Lista_f07b3200(Path caminho) throws IOException {
        try (Stream<Path> entrada_VALOR_962f286b = Files.list(caminho)) { return entrada_VALOR_962f286b.sorted().collect(Collectors.toList()); }
    }
}
