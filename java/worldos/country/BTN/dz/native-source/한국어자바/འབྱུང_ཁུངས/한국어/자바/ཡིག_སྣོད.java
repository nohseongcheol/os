// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 ཡིག_སྣོད 도우미. */
public final class ཡིག_སྣོད {
    private ཡིག_སྣོད() {}
    public static Path འགྲུལ_ལམ(String མིང) { return Path.of(མིང); }
    public static String ལྷག(Path འགྲུལ_ལམ) throws IOException {
        return Files.readString(འགྲུལ_ལམ, StandardCharsets.UTF_8);
    }
    public static Path བྲིས(Path འགྲུལ_ལམ, String 내용) throws IOException {
        return Files.writeString(འགྲུལ_ལམ, 내용, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path འགྲུལ_ལམ) throws IOException { return Files.readAllBytes(འགྲུལ_ལམ); }
    public static Path 바이트쓰기(Path འགྲུལ_ལམ, byte[] 내용) throws IOException { return Files.write(འགྲུལ_ལམ, 내용); }
    public static Path 폴더만들기(Path འགྲུལ_ལམ) throws IOException { return Files.createDirectories(འགྲུལ_ལམ); }
    public static boolean 있는가(Path འགྲུལ_ལམ) { return Files.exists(འགྲུལ_ལམ); }
    public static boolean 지우기(Path འགྲུལ_ལམ) throws IOException { return Files.deleteIfExists(འགྲུལ_ལམ); }
    public static List<Path> 목록(Path འགྲུལ_ལམ) throws IOException {
        try (Stream<Path> 항목 = Files.list(འགྲུལ_ལམ)) { return 항목.sorted().collect(Collectors.toList()); }
    }
}
