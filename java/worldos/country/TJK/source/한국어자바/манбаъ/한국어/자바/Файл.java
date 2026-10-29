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
    public static Path масир(String Ном) { return Path.of(Ном); }
    public static String Хондан(Path масир) throws IOException {
        return Files.readString(масир, StandardCharsets.UTF_8);
    }
    public static Path Навиштан(Path масир, String Мӯҳтаво_қимат) throws IOException {
        return Files.writeString(масир, Мӯҳтаво_қимат, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path масир) throws IOException { return Files.readAllBytes(масир); }
    public static Path навиштан_байт_қимат(Path масир, byte[] Мӯҳтаво_қимат) throws IOException { return Files.write(масир, Мӯҳтаво_қимат); }
    public static Path эҷод_кардан_директория(Path масир) throws IOException { return Files.createDirectories(масир); }
    public static boolean 있는가(Path масир) { return Files.exists(масир); }
    public static boolean 지우기(Path масир) throws IOException { return Files.deleteIfExists(масир); }
    public static List<Path> ворида_Рӯйхат(Path масир) throws IOException {
        try (Stream<Path> ворида_қимат = Files.list(масир)) { return ворида_қимат.sorted().collect(Collectors.toList()); }
    }
}
