// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 Fichier 도우미. */
public final class Fichier {
    private Fichier() {}
    public static Path Wee(String Numm) { return Path.of(Numm); }
    public static String 읽기(Path Wee) throws IOException {
        return Files.readString(Wee, StandardCharsets.UTF_8);
    }
    public static Path schreiwen(Path Wee, String Inhalt_VALUE) throws IOException {
        return Files.writeString(Wee, Inhalt_VALUE, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path Wee) throws IOException { return Files.readAllBytes(Wee); }
    public static Path schreiwen_Byte_VALUE(Path Wee, byte[] Inhalt_VALUE) throws IOException { return Files.write(Wee, Inhalt_VALUE); }
    public static Path Create_Verzeechnes(Path Wee) throws IOException { return Files.createDirectories(Wee); }
    public static boolean 있는가(Path Wee) { return Files.exists(Wee); }
    public static boolean 지우기(Path Wee) throws IOException { return Files.deleteIfExists(Wee); }
    public static List<Path> Agab_Lëscht(Path Wee) throws IOException {
        try (Stream<Path> Agab_VALUE = Files.list(Wee)) { return Agab_VALUE.sorted().collect(Collectors.toList()); }
    }
}
