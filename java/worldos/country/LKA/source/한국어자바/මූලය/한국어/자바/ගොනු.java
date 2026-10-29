// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 ගොනු 도우미. */
public final class ගොනු {
    private ගොනු() {}
    public static Path මාර්_ගය(String නම) { return Path.of(නම); }
    public static String කියවීම(Path මාර්_ගය) throws IOException {
        return Files.readString(මාර්_ගය, StandardCharsets.UTF_8);
    }
    public static Path ලිවීම(Path මාර්_ගය, String අන්තර්ගතය_අගය) throws IOException {
        return Files.writeString(මාර්_ගය, අන්තර්ගතය_අගය, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path මාර්_ගය) throws IOException { return Files.readAllBytes(මාර්_ගය); }
    public static Path ලියන්න_බයිටය_අගය(Path මාර්_ගය, byte[] අන්තර්ගතය_අගය) throws IOException { return Files.write(මාර්_ගය, අන්තර්ගතය_අගය); }
    public static Path සාදන්න_නාමාවලිය(Path මාර්_ගය) throws IOException { return Files.createDirectories(මාර්_ගය); }
    public static boolean 있는가(Path මාර්_ගය) { return Files.exists(මාර්_ගය); }
    public static boolean 지우기(Path මාර්_ගය) throws IOException { return Files.deleteIfExists(මාර්_ගය); }
    public static List<Path> පිවිසුම_ලැයිස්තුව(Path මාර්_ගය) throws IOException {
        try (Stream<Path> පිවිසුම_අගය = Files.list(මාර්_ගය)) { return පිවිසුම_අගය.sorted().collect(Collectors.toList()); }
    }
}
