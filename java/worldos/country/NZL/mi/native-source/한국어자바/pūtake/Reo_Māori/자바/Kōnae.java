// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Reo_Māori.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 Kōnae 도우미. */
public final class Kōnae {
    private Kōnae() {}
    public static Path ara(String Ingoa) { return Path.of(Ingoa); }
    public static String Pānuitia(Path ara) throws IOException {
        return Files.readString(ara, StandardCharsets.UTF_8);
    }
    public static Path Tuhia(Path ara, String Ihirangi_uara) throws IOException {
        return Files.writeString(ara, Ihirangi_uara, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path ara) throws IOException { return Files.readAllBytes(ara); }
    public static Path tuhi_paita_uara(Path ara, byte[] Ihirangi_uara) throws IOException { return Files.write(ara, Ihirangi_uara); }
    public static Path Waihanga_whaiaronga(Path ara) throws IOException { return Files.createDirectories(ara); }
    public static boolean 있는가(Path ara) { return Files.exists(ara); }
    public static boolean 지우기(Path ara) throws IOException { return Files.deleteIfExists(ara); }
    public static List<Path> tāurunga_Rārangi(Path ara) throws IOException {
        try (Stream<Path> tāurunga_uara = Files.list(ara)) { return tāurunga_uara.sorted().collect(Collectors.toList()); }
    }
}
