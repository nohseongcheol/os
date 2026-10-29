// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eesti.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 Fail 도우미. */
public final class Fail {
    private Fail() {}
    public static Path RADA(String Nimi_2) { return Path.of(Nimi_2); }
    public static String Lugemine(Path RADA) throws IOException {
        return Files.readString(RADA, StandardCharsets.UTF_8);
    }
    public static Path Kirjutamine(Path RADA, String Sisu_VALUE) throws IOException {
        return Files.writeString(RADA, Sisu_VALUE, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path RADA) throws IOException { return Files.readAllBytes(RADA); }
    public static Path kirjutamine_bait_VALUE(Path RADA, byte[] Sisu_VALUE) throws IOException { return Files.write(RADA, Sisu_VALUE); }
    public static Path avama_kaust(Path RADA) throws IOException { return Files.createDirectories(RADA); }
    public static boolean 있는가(Path RADA) { return Files.exists(RADA); }
    public static boolean kustutama_kirje(Path RADA) throws IOException { return Files.deleteIfExists(RADA); }
    public static List<Path> kirje_Loend(Path RADA) throws IOException {
        try (Stream<Path> kirje_VALUE = Files.list(RADA)) { return kirje_VALUE.sorted().collect(Collectors.toList()); }
    }
}
