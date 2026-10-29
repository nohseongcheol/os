// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Gaeilge.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 Comhad 도우미. */
public final class Comhad {
    private Comhad() {}
    public static Path CONAIR(String Ainm) { return Path.of(Ainm); }
    public static String Léigh(Path CONAIR) throws IOException {
        return Files.readString(CONAIR, StandardCharsets.UTF_8);
    }
    public static Path Scríobh(Path CONAIR, String Inneachar_VALUE) throws IOException {
        return Files.writeString(CONAIR, Inneachar_VALUE, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path CONAIR) throws IOException { return Files.readAllBytes(CONAIR); }
    public static Path scríobh_beart_VALUE(Path CONAIR, byte[] Inneachar_VALUE) throws IOException { return Files.write(CONAIR, Inneachar_VALUE); }
    public static Path Create_eolaire(Path CONAIR) throws IOException { return Files.createDirectories(CONAIR); }
    public static boolean 있는가(Path CONAIR) { return Files.exists(CONAIR); }
    public static boolean 지우기(Path CONAIR) throws IOException { return Files.deleteIfExists(CONAIR); }
    public static List<Path> iontráil_Liosta(Path CONAIR) throws IOException {
        try (Stream<Path> iontráil_VALUE = Files.list(CONAIR)) { return iontráil_VALUE.sorted().collect(Collectors.toList()); }
    }
}
