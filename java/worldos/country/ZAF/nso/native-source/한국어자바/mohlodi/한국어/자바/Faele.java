// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 Faele 도우미. */
public final class Faele {
    private Faele() {}
    public static Path Tsejana(String Leina) { return Path.of(Leina); }
    public static String Bala(Path Tsejana) throws IOException {
        return Files.readString(Tsejana, StandardCharsets.UTF_8);
    }
    public static Path Ngwala(Path Tsejana, String Diteng_boleng) throws IOException {
        return Files.writeString(Tsejana, Diteng_boleng, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path Tsejana) throws IOException { return Files.readAllBytes(Tsejana); }
    public static Path ngwala_paete_boleng(Path Tsejana, byte[] Diteng_boleng) throws IOException { return Files.write(Tsejana, Diteng_boleng); }
    public static Path 폴더만들기(Path Tsejana) throws IOException { return Files.createDirectories(Tsejana); }
    public static boolean 있는가(Path Tsejana) { return Files.exists(Tsejana); }
    public static boolean 지우기(Path Tsejana) throws IOException { return Files.deleteIfExists(Tsejana); }
    public static List<Path> go_tsenya_tshedimošo_Lenaneo(Path Tsejana) throws IOException {
        try (Stream<Path> go_tsenya_tshedimošo_boleng = Files.list(Tsejana)) { return go_tsenya_tshedimošo_boleng.sorted().collect(Collectors.toList()); }
    }
}
