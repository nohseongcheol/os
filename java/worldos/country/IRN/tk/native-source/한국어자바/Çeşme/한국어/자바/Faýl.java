// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 Faýl 도우미. */
public final class Faýl {
    private Faýl() {}
    public static Path Ýol(String Ad) { return Path.of(Ad); }
    public static String Oka(Path Ýol) throws IOException {
        return Files.readString(Ýol, StandardCharsets.UTF_8);
    }
    public static Path Ýaz(Path Ýol, String Mazmun_baha) throws IOException {
        return Files.writeString(Ýol, Mazmun_baha, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path Ýol) throws IOException { return Files.readAllBytes(Ýol); }
    public static Path ýaz_baýt_baha(Path Ýol, byte[] Mazmun_baha) throws IOException { return Files.write(Ýol, Mazmun_baha); }
    public static Path döretmek_katalog(Path Ýol) throws IOException { return Files.createDirectories(Ýol); }
    public static boolean 있는가(Path Ýol) { return Files.exists(Ýol); }
    public static boolean 지우기(Path Ýol) throws IOException { return Files.deleteIfExists(Ýol); }
    public static List<Path> girizmeklik_Sanaw(Path Ýol) throws IOException {
        try (Stream<Path> girizmeklik_baha = Files.list(Ýol)) { return girizmeklik_baha.sorted().collect(Collectors.toList()); }
    }
}
