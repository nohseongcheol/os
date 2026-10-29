// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 faili 도우미. */
public final class faili {
    private faili() {}
    public static Path njia(String Jina) { return Path.of(Jina); }
    public static String 읽기(Path njia) throws IOException {
        return Files.readString(njia, StandardCharsets.UTF_8);
    }
    public static Path andika(Path njia, String maudhui_thamani) throws IOException {
        return Files.writeString(njia, maudhui_thamani, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path njia) throws IOException { return Files.readAllBytes(njia); }
    public static Path andika_baiti_thamani(Path njia, byte[] maudhui_thamani) throws IOException { return Files.write(njia, maudhui_thamani); }
    public static Path unda_Saraka(Path njia) throws IOException { return Files.createDirectories(njia); }
    public static boolean 있는가(Path njia) { return Files.exists(njia); }
    public static boolean futa_ingizo(Path njia) throws IOException { return Files.deleteIfExists(njia); }
    public static List<Path> ingizo_Orodha(Path njia) throws IOException {
        try (Stream<Path> ingizo_thamani = Files.list(njia)) { return ingizo_thamani.sorted().collect(Collectors.toList()); }
    }
}
