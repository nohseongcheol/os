// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package čeština.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 název_souboru pomocná_rutina_HODNOTA. */
public final class název_souboru {
    private název_souboru() {}
    public static Path cesta_2(String Název) { return Path.of(Název); }
    public static String Čtení(Path cesta_2) throws IOException {
        return Files.readString(cesta_2, StandardCharsets.UTF_8);
    }
    public static Path Zápis(Path cesta_2, String Obsah_HODNOTA) throws IOException {
        return Files.writeString(cesta_2, Obsah_HODNOTA, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path cesta_2) throws IOException { return Files.readAllBytes(cesta_2); }
    public static Path zápis_bajt_HODNOTA(Path cesta_2, byte[] Obsah_HODNOTA) throws IOException { return Files.write(cesta_2, Obsah_HODNOTA); }
    public static Path Create_Adresář(Path cesta_2) throws IOException { return Files.createDirectories(cesta_2); }
    public static boolean 있는가(Path cesta_2) { return Files.exists(cesta_2); }
    public static boolean vymazat_položka(Path cesta_2) throws IOException { return Files.deleteIfExists(cesta_2); }
    public static List<Path> položka_Seznam(Path cesta_2) throws IOException {
        try (Stream<Path> položka_HODNOTA = Files.list(cesta_2)) { return položka_HODNOTA.sorted().collect(Collectors.toList()); }
    }
}
