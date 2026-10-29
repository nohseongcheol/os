// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 COADAN 도우미. */
public final class COADAN {
    private COADAN() {}
    public static Path 경로(String 이름) { return Path.of(이름); }
    public static String 읽기(Path 경로) throws IOException {
        return Files.readString(경로, StandardCharsets.UTF_8);
    }
    public static Path 쓰기(Path 경로, String 내용) throws IOException {
        return Files.writeString(경로, 내용, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path 경로) throws IOException { return Files.readAllBytes(경로); }
    public static Path 바이트쓰기(Path 경로, byte[] 내용) throws IOException { return Files.write(경로, 내용); }
    public static Path 폴더만들기(Path 경로) throws IOException { return Files.createDirectories(경로); }
    public static boolean 있는가(Path 경로) { return Files.exists(경로); }
    public static boolean 지우기(Path 경로) throws IOException { return Files.deleteIfExists(경로); }
    public static List<Path> 목록(Path 경로) throws IOException {
        try (Stream<Path> 항목 = Files.list(경로)) { return 항목.sorted().collect(Collectors.toList()); }
    }
}
