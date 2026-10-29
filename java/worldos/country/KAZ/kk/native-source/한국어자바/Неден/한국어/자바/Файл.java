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
    public static Path Жол_2(String Аты) { return Path.of(Аты); }
    public static String Оқу(Path Жол_2) throws IOException {
        return Files.readString(Жол_2, StandardCharsets.UTF_8);
    }
    public static Path Жазу(Path Жол_2, String мазмұн_мән) throws IOException {
        return Files.writeString(Жол_2, мазмұн_мән, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path Жол_2) throws IOException { return Files.readAllBytes(Жол_2); }
    public static Path жазу_байт_мән(Path Жол_2, byte[] мазмұн_мән) throws IOException { return Files.write(Жол_2, мазмұн_мән); }
    public static Path жасау_каталог(Path Жол_2) throws IOException { return Files.createDirectories(Жол_2); }
    public static boolean 있는가(Path Жол_2) { return Files.exists(Жол_2); }
    public static boolean өшіру_енгізу(Path Жол_2) throws IOException { return Files.deleteIfExists(Жол_2); }
    public static List<Path> енгізу_Тізім(Path Жол_2) throws IOException {
        try (Stream<Path> енгізу_мән = Files.list(Жол_2)) { return енгізу_мән.sorted().collect(Collectors.toList()); }
    }
}
