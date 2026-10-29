// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 Файл 도우미. */
public final class Файл {
    private Файл() {}
    public static Path ШЛЯХ(String Назва) { return Path.of(Назва); }
    public static String Чытанне(Path ШЛЯХ) throws IOException {
        return Files.readString(ШЛЯХ, StandardCharsets.UTF_8);
    }
    public static Path Запіс(Path ШЛЯХ, String кантэнт_значэнне) throws IOException {
        return Files.writeString(ШЛЯХ, кантэнт_значэнне, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path ШЛЯХ) throws IOException { return Files.readAllBytes(ШЛЯХ); }
    public static Path напісаць_байт_значэнне(Path ШЛЯХ, byte[] кантэнт_значэнне) throws IOException { return Files.write(ШЛЯХ, кантэнт_значэнне); }
    public static Path стварыць_каталог(Path ШЛЯХ) throws IOException { return Files.createDirectories(ШЛЯХ); }
    public static boolean 있는가(Path ШЛЯХ) { return Files.exists(ШЛЯХ); }
    public static boolean ачысціць_увядзенне(Path ШЛЯХ) throws IOException { return Files.deleteIfExists(ШЛЯХ); }
    public static List<Path> увядзенне_Спіс(Path ШЛЯХ) throws IOException {
        try (Stream<Path> увядзенне_значэнне = Files.list(ШЛЯХ)) { return увядзенне_значэнне.sorted().collect(Collectors.toList()); }
    }
}
