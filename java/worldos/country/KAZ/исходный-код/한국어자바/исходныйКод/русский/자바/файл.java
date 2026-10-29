// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package русский.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 файл вспомогательное_приложение_ЗНАЧЕН. */
public final class файл {
    private файл() {}
    public static Path путь(String Название) { return Path.of(Название); }
    public static String Чтение(Path путь) throws IOException {
        return Files.readString(путь, StandardCharsets.UTF_8);
    }
    public static Path Запись(Path путь, String контент_ЗНАЧЕН) throws IOException {
        return Files.writeString(путь, контент_ЗНАЧЕН, StandardCharsets.UTF_8);
    }
    public static byte[] чтение_байт_ЗНАЧЕН(Path путь) throws IOException { return Files.readAllBytes(путь); }
    public static Path запись_байт_ЗНАЧЕН(Path путь, byte[] контент_ЗНАЧЕН) throws IOException { return Files.write(путь, контент_ЗНАЧЕН); }
    public static Path Create_Каталог(Path путь) throws IOException { return Files.createDirectories(путь); }
    public static boolean 있는가(Path путь) { return Files.exists(путь); }
    public static boolean удалить_ввод_c8dbc399(Path путь) throws IOException { return Files.deleteIfExists(путь); }
    public static List<Path> ввод_Список(Path путь) throws IOException {
        try (Stream<Path> ввод_ЗНАЧЕН = Files.list(путь)) { return ввод_ЗНАЧЕН.sorted().collect(Collectors.toList()); }
    }
}
