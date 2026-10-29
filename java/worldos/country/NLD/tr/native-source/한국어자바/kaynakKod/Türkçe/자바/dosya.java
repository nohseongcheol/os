// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Türkçe.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 dosya yardımcı_değer. */
public final class dosya {
    private dosya() {}
    public static Path yol(String İsim) { return Path.of(İsim); }
    public static String Okuma(Path yol) throws IOException {
        return Files.readString(yol, StandardCharsets.UTF_8);
    }
    public static Path Yazma(Path yol, String içerik_değer) throws IOException {
        return Files.writeString(yol, içerik_değer, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path yol) throws IOException { return Files.readAllBytes(yol); }
    public static Path yazma_bayt_değer(Path yol, byte[] içerik_değer) throws IOException { return Files.write(yol, içerik_değer); }
    public static Path açmak_dizin(Path yol) throws IOException { return Files.createDirectories(yol); }
    public static boolean 있는가(Path yol) { return Files.exists(yol); }
    public static boolean silmek_girdi(Path yol) throws IOException { return Files.deleteIfExists(yol); }
    public static List<Path> girdi_Liste(Path yol) throws IOException {
        try (Stream<Path> girdi_değer = Files.list(yol)) { return girdi_değer.sorted().collect(Collectors.toList()); }
    }
}
