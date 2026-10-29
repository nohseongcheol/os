// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 फाइल 도우미. */
public final class फाइल {
    private फाइल() {}
    public static Path पथ(String नाम) { return Path.of(नाम); }
    public static String पढ़ू(Path पथ) throws IOException {
        return Files.readString(पथ, StandardCharsets.UTF_8);
    }
    public static Path लिखू(Path पथ, String 내용) throws IOException {
        return Files.writeString(पथ, 내용, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path पथ) throws IOException { return Files.readAllBytes(पथ); }
    public static Path 바이트쓰기(Path पथ, byte[] 내용) throws IOException { return Files.write(पथ, 내용); }
    public static Path 폴더만들기(Path पथ) throws IOException { return Files.createDirectories(पथ); }
    public static boolean 있는가(Path पथ) { return Files.exists(पथ); }
    public static boolean 지우기(Path पथ) throws IOException { return Files.deleteIfExists(पथ); }
    public static List<Path> 목록(Path पथ) throws IOException {
        try (Stream<Path> 항목 = Files.list(पथ)) { return 항목.sorted().collect(Collectors.toList()); }
    }
}
