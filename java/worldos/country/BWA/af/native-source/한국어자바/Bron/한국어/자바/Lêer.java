// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 Lêer 도우미. */
public final class Lêer {
    private Lêer() {}
    public static Path Pad(String Naam) { return Path.of(Naam); }
    public static String Lees(Path Pad) throws IOException {
        return Files.readString(Pad, StandardCharsets.UTF_8);
    }
    public static Path Skryf(Path Pad, String Inhoud_VALUE) throws IOException {
        return Files.writeString(Pad, Inhoud_VALUE, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path Pad) throws IOException { return Files.readAllBytes(Pad); }
    public static Path skryf_greep_VALUE(Path Pad, byte[] Inhoud_VALUE) throws IOException { return Files.write(Pad, Inhoud_VALUE); }
    public static Path Skep_gids(Path Pad) throws IOException { return Files.createDirectories(Pad); }
    public static boolean 있는가(Path Pad) { return Files.exists(Pad); }
    public static boolean vee_uit_inskrywing(Path Pad) throws IOException { return Files.deleteIfExists(Pad); }
    public static List<Path> inskrywing_Lys(Path Pad) throws IOException {
        try (Stream<Path> inskrywing_VALUE = Files.list(Pad)) { return inskrywing_VALUE.sorted().collect(Collectors.toList()); }
    }
}
