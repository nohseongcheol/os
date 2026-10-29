// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package español.Java;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** Herramienta de archivos UTF-8 que usa directamente Path e IOException estándar. */
public final class Archivo {
    private Archivo() {}
    public static Path ruta(String nombre) { return Path.of(nombre); }
    public static String leer(Path ruta) throws IOException {
        return Files.readString(ruta, StandardCharsets.UTF_8);
    }
    public static Path escribir(Path ruta, String valorContenidoValor) throws IOException {
        return Files.writeString(ruta, valorContenidoValor, StandardCharsets.UTF_8);
    }
    public static byte[] leerValorByte(Path ruta) throws IOException { return Files.readAllBytes(ruta); }
    public static Path escribirValorByte(Path ruta, byte[] valorContenidoValor) throws IOException { return Files.write(ruta, valorContenidoValor); }
    public static Path crearDirectorio(Path ruta) throws IOException { return Files.createDirectories(ruta); }
    public static boolean efectúaExistencia(Path ruta) { return Files.exists(ruta); }
    public static boolean borrarEntradaElemento(Path ruta) throws IOException { return Files.deleteIfExists(ruta); }
    public static List<Path> listaEntradaElemento(Path ruta) throws IOException {
        try (Stream<Path> valorEntradaElemento = Files.list(ruta)) { return valorEntradaElemento.sorted().collect(Collectors.toList()); }
    }
}
