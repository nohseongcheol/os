// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 Pel 도우미. */
public final class Pel {
    private Pel() {}
    public static Path RÊ(String Nav) { return Path.of(Nav); }
    public static String Bixwîne(Path RÊ) throws IOException {
        return Files.readString(RÊ, StandardCharsets.UTF_8);
    }
    public static Path Binivîse(Path RÊ, String 내용) throws IOException {
        return Files.writeString(RÊ, 내용, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path RÊ) throws IOException { return Files.readAllBytes(RÊ); }
    public static Path 바이트쓰기(Path RÊ, byte[] 내용) throws IOException { return Files.write(RÊ, 내용); }
    public static Path 폴더만들기(Path RÊ) throws IOException { return Files.createDirectories(RÊ); }
    public static boolean 있는가(Path RÊ) { return Files.exists(RÊ); }
    public static boolean 지우기(Path RÊ) throws IOException { return Files.deleteIfExists(RÊ); }
    public static List<Path> 목록(Path RÊ) throws IOException {
        try (Stream<Path> 항목 = Files.list(RÊ)) { return 항목.sorted().collect(Collectors.toList()); }
    }
}
