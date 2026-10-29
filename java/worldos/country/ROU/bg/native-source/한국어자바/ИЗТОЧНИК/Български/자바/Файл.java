// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Български.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 Файл 도우미. */
public final class Файл {
    private Файл() {}
    public static Path ПЪТ(String Име) { return Path.of(Име); }
    public static String Четене(Path ПЪТ) throws IOException {
        return Files.readString(ПЪТ, StandardCharsets.UTF_8);
    }
    public static Path Писане(Path ПЪТ, String Съдържание_стойност) throws IOException {
        return Files.writeString(ПЪТ, Съдържание_стойност, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path ПЪТ) throws IOException { return Files.readAllBytes(ПЪТ); }
    public static Path записване_байт_стойност(Path ПЪТ, byte[] Съдържание_стойност) throws IOException { return Files.write(ПЪТ, Съдържание_стойност); }
    public static Path Създаване_указател(Path ПЪТ) throws IOException { return Files.createDirectories(ПЪТ); }
    public static boolean 있는가(Path ПЪТ) { return Files.exists(ПЪТ); }
    public static boolean изтривам_запис(Path ПЪТ) throws IOException { return Files.deleteIfExists(ПЪТ); }
    public static List<Path> запис_Списък(Path ПЪТ) throws IOException {
        try (Stream<Path> запис_стойност = Files.list(ПЪТ)) { return запис_стойност.sorted().collect(Collectors.toList()); }
    }
}
