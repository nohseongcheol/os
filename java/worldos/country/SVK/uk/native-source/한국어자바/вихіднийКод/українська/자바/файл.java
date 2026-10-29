// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package українська.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 файл 도우미. */
public final class файл {
    private файл() {}
    public static Path шлях(String Назва) { return Path.of(Назва); }
    public static String Читання(Path шлях) throws IOException {
        return Files.readString(шлях, StandardCharsets.UTF_8);
    }
    public static Path Запис(Path шлях, String Вміст_значення) throws IOException {
        return Files.writeString(шлях, Вміст_значення, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path шлях) throws IOException { return Files.readAllBytes(шлях); }
    public static Path записування_байт_значення(Path шлях, byte[] Вміст_значення) throws IOException { return Files.write(шлях, Вміст_значення); }
    public static Path Створення_Каталог(Path шлях) throws IOException { return Files.createDirectories(шлях); }
    public static boolean 있는가(Path шлях) { return Files.exists(шлях); }
    public static boolean видаляти_запис(Path шлях) throws IOException { return Files.deleteIfExists(шлях); }
    public static List<Path> запис_список(Path шлях) throws IOException {
        try (Stream<Path> запис_значення_962f286b = Files.list(шлях)) { return запис_значення_962f286b.sorted().collect(Collectors.toList()); }
    }
}
