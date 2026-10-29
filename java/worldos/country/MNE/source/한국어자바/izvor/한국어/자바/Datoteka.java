// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 Datoteka 도우미. */
public final class Datoteka {
    private Datoteka() {}
    public static Path putanja(String ime) { return Path.of(ime); }
    public static String 읽기(Path putanja) throws IOException {
        return Files.readString(putanja, StandardCharsets.UTF_8);
    }
    public static Path 쓰기(Path putanja, String Sadržaj_VALUE) throws IOException {
        return Files.writeString(putanja, Sadržaj_VALUE, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path putanja) throws IOException { return Files.readAllBytes(putanja); }
    public static Path 바이트쓰기(Path putanja, byte[] Sadržaj_VALUE) throws IOException { return Files.write(putanja, Sadržaj_VALUE); }
    public static Path Create_Imenik(Path putanja) throws IOException { return Files.createDirectories(putanja); }
    public static boolean 있는가(Path putanja) { return Files.exists(putanja); }
    public static boolean obrisati_stavka(Path putanja) throws IOException { return Files.deleteIfExists(putanja); }
    public static List<Path> stavka_Lista(Path putanja) throws IOException {
        try (Stream<Path> stavka_VALUE = Files.list(putanja)) { return stavka_VALUE.sorted().collect(Collectors.toList()); }
    }
}
