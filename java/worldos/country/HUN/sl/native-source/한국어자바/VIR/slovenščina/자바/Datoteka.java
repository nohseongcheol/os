// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package slovenščina.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 Datoteka 도우미. */
public final class Datoteka {
    private Datoteka() {}
    public static Path POT(String Ime) { return Path.of(Ime); }
    public static String Branje(Path POT) throws IOException {
        return Files.readString(POT, StandardCharsets.UTF_8);
    }
    public static Path Pisanje(Path POT, String vsebina_VALUE) throws IOException {
        return Files.writeString(POT, vsebina_VALUE, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path POT) throws IOException { return Files.readAllBytes(POT); }
    public static Path pisati_bajt_VALUE(Path POT, byte[] vsebina_VALUE) throws IOException { return Files.write(POT, vsebina_VALUE); }
    public static Path Ustvari_Imenik(Path POT) throws IOException { return Files.createDirectories(POT); }
    public static boolean 있는가(Path POT) { return Files.exists(POT); }
    public static boolean izbrisati_vnos(Path POT) throws IOException { return Files.deleteIfExists(POT); }
    public static List<Path> vnos_Seznam(Path POT) throws IOException {
        try (Stream<Path> vnos_VALUE = Files.list(POT)) { return vnos_VALUE.sorted().collect(Collectors.toList()); }
    }
}
