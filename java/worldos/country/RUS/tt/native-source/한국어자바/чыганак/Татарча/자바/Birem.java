// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Татарча.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 Birem 도우미. */
public final class Birem {
    private Birem() {}
    public static Path Yul(String исем) { return Path.of(исем); }
    public static String 읽기(Path Yul) throws IOException {
        return Files.readString(Yul, StandardCharsets.UTF_8);
    }
    public static Path язу(Path Yul, String Эчтәлек_VALUE) throws IOException {
        return Files.writeString(Yul, Эчтәлек_VALUE, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path Yul) throws IOException { return Files.readAllBytes(Yul); }
    public static Path язу_байт_VALUE(Path Yul, byte[] Эчтәлек_VALUE) throws IOException { return Files.write(Yul, Эчтәлек_VALUE); }
    public static Path Төзү_каталог(Path Yul) throws IOException { return Files.createDirectories(Yul); }
    public static boolean 있는가(Path Yul) { return Files.exists(Yul); }
    public static boolean 지우기(Path Yul) throws IOException { return Files.deleteIfExists(Yul); }
    public static List<Path> кертү_Исемлек(Path Yul) throws IOException {
        try (Stream<Path> кертү_VALUE = Files.list(Yul)) { return кертү_VALUE.sorted().collect(Collectors.toList()); }
    }
}
