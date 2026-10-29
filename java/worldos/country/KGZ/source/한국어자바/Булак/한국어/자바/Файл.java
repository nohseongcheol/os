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
    public static Path ЖОЛ(String Аты) { return Path.of(Аты); }
    public static String Окуу(Path ЖОЛ) throws IOException {
        return Files.readString(ЖОЛ, StandardCharsets.UTF_8);
    }
    public static Path Жазуу(Path ЖОЛ, String Мазмун_маани) throws IOException {
        return Files.writeString(ЖОЛ, Мазмун_маани, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path ЖОЛ) throws IOException { return Files.readAllBytes(ЖОЛ); }
    public static Path жазуу_байт_маани(Path ЖОЛ, byte[] Мазмун_маани) throws IOException { return Files.write(ЖОЛ, Мазмун_маани); }
    public static Path түзүү_каталог(Path ЖОЛ) throws IOException { return Files.createDirectories(ЖОЛ); }
    public static boolean 있는가(Path ЖОЛ) { return Files.exists(ЖОЛ); }
    public static boolean 지우기(Path ЖОЛ) throws IOException { return Files.deleteIfExists(ЖОЛ); }
    public static List<Path> киргизме_жазуу_Тизме(Path ЖОЛ) throws IOException {
        try (Stream<Path> киргизме_жазуу_маани = Files.list(ЖОЛ)) { return киргизме_жазуу_маани.sorted().collect(Collectors.toList()); }
    }
}
