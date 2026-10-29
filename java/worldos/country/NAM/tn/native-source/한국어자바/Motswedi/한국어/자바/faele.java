// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 faele 도우미. */
public final class faele {
    private faele() {}
    public static Path tsela(String leina) { return Path.of(leina); }
    public static String 읽기(Path tsela) throws IOException {
        return Files.readString(tsela, StandardCharsets.UTF_8);
    }
    public static Path kwala(Path tsela, String Diteng_Boleng) throws IOException {
        return Files.writeString(tsela, Diteng_Boleng, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path tsela) throws IOException { return Files.readAllBytes(tsela); }
    public static Path kwala_baete_Boleng(Path tsela, byte[] Diteng_Boleng) throws IOException { return Files.write(tsela, Diteng_Boleng); }
    public static Path tlhama_Lenaneofaele(Path tsela) throws IOException { return Files.createDirectories(tsela); }
    public static boolean 있는가(Path tsela) { return Files.exists(tsela); }
    public static boolean 지우기(Path tsela) throws IOException { return Files.deleteIfExists(tsela); }
    public static List<Path> tsenyo_lenaane(Path tsela) throws IOException {
        try (Stream<Path> tsenyo_Boleng = Files.list(tsela)) { return tsenyo_Boleng.sorted().collect(Collectors.toList()); }
    }
}
