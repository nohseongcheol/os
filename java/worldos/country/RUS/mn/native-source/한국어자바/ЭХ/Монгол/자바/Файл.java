// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Монгол.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 Файл 도우미. */
public final class Файл {
    private Файл() {}
    public static Path ЗАМ(String Нэр) { return Path.of(Нэр); }
    public static String Унших(Path ЗАМ) throws IOException {
        return Files.readString(ЗАМ, StandardCharsets.UTF_8);
    }
    public static Path Бичих(Path ЗАМ, String Агуулга_утга) throws IOException {
        return Files.writeString(ЗАМ, Агуулга_утга, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path ЗАМ) throws IOException { return Files.readAllBytes(ЗАМ); }
    public static Path бичих_байт_утга(Path ЗАМ, byte[] Агуулга_утга) throws IOException { return Files.write(ЗАМ, Агуулга_утга); }
    public static Path үүсгэх_лавлах(Path ЗАМ) throws IOException { return Files.createDirectories(ЗАМ); }
    public static boolean 있는가(Path ЗАМ) { return Files.exists(ЗАМ); }
    public static boolean 지우기(Path ЗАМ) throws IOException { return Files.deleteIfExists(ЗАМ); }
    public static List<Path> оролт_Жагсаалт(Path ЗАМ) throws IOException {
        try (Stream<Path> оролт_утга = Files.list(ЗАМ)) { return оролт_утга.sorted().collect(Collectors.toList()); }
    }
}
