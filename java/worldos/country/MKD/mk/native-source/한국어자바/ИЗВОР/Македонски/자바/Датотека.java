// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Македонски.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 Датотека 도우미. */
public final class Датотека {
    private Датотека() {}
    public static Path ПАТЕКА(String Име) { return Path.of(Име); }
    public static String Читај(Path ПАТЕКА) throws IOException {
        return Files.readString(ПАТЕКА, StandardCharsets.UTF_8);
    }
    public static Path Запиши(Path ПАТЕКА, String Содржина_VALUE) throws IOException {
        return Files.writeString(ПАТЕКА, Содржина_VALUE, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path ПАТЕКА) throws IOException { return Files.readAllBytes(ПАТЕКА); }
    public static Path запиши_бајт_VALUE(Path ПАТЕКА, byte[] Содржина_VALUE) throws IOException { return Files.write(ПАТЕКА, Содржина_VALUE); }
    public static Path Create_Именик(Path ПАТЕКА) throws IOException { return Files.createDirectories(ПАТЕКА); }
    public static boolean 있는가(Path ПАТЕКА) { return Files.exists(ПАТЕКА); }
    public static boolean избриши_внес(Path ПАТЕКА) throws IOException { return Files.deleteIfExists(ПАТЕКА); }
    public static List<Path> внес_Список(Path ПАТЕКА) throws IOException {
        try (Stream<Path> внес_VALUE = Files.list(ПАТЕКА)) { return внес_VALUE.sorted().collect(Collectors.toList()); }
    }
}
