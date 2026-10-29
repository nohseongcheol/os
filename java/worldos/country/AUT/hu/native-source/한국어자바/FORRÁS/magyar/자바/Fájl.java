// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package magyar.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 Fájl segéd_ÉRTÉK. */
public final class Fájl {
    private Fájl() {}
    public static Path ÚTVONAL(String Név) { return Path.of(Név); }
    public static String Olvasás(Path ÚTVONAL) throws IOException {
        return Files.readString(ÚTVONAL, StandardCharsets.UTF_8);
    }
    public static Path Írás(Path ÚTVONAL, String Tartalom_ÉRTÉK) throws IOException {
        return Files.writeString(ÚTVONAL, Tartalom_ÉRTÉK, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path ÚTVONAL) throws IOException { return Files.readAllBytes(ÚTVONAL); }
    public static Path ír_bájt_ÉRTÉK(Path ÚTVONAL, byte[] Tartalom_ÉRTÉK) throws IOException { return Files.write(ÚTVONAL, Tartalom_ÉRTÉK); }
    public static Path készít_címtár(Path ÚTVONAL) throws IOException { return Files.createDirectories(ÚTVONAL); }
    public static boolean 있는가(Path ÚTVONAL) { return Files.exists(ÚTVONAL); }
    public static boolean töröl_bejegyzés(Path ÚTVONAL) throws IOException { return Files.deleteIfExists(ÚTVONAL); }
    public static List<Path> bejegyzés_Lista(Path ÚTVONAL) throws IOException {
        try (Stream<Path> bejegyzés_ÉRTÉK = Files.list(ÚTVONAL)) { return bejegyzés_ÉRTÉK.sorted().collect(Collectors.toList()); }
    }
}
