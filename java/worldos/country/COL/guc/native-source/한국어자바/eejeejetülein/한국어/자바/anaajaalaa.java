// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 anaajaalaa 도우미. */
public final class anaajaalaa {
    private anaajaalaa() {}
    public static Path wopu_a_ttaaleemüin(String 이름) { return Path.of(이름); }
    public static String 읽기(Path wopu_a_ttaaleemüin) throws IOException {
        return Files.readString(wopu_a_ttaaleemüin, StandardCharsets.UTF_8);
    }
    public static Path ashajaa(Path wopu_a_ttaaleemüin, String alu_ujatüü_ajutuu) throws IOException {
        return Files.writeString(wopu_a_ttaaleemüin, alu_ujatüü_ajutuu, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path wopu_a_ttaaleemüin) throws IOException { return Files.readAllBytes(wopu_a_ttaaleemüin); }
    public static Path ashajaa_waai_ajutuu(Path wopu_a_ttaaleemüin, byte[] alu_ujatüü_ajutuu) throws IOException { return Files.write(wopu_a_ttaaleemüin, alu_ujatüü_ajutuu); }
    public static Path 폴더만들기(Path wopu_a_ttaaleemüin) throws IOException { return Files.createDirectories(wopu_a_ttaaleemüin); }
    public static boolean 있는가(Path wopu_a_ttaaleemüin) { return Files.exists(wopu_a_ttaaleemüin); }
    public static boolean 지우기(Path wopu_a_ttaaleemüin) throws IOException { return Files.deleteIfExists(wopu_a_ttaaleemüin); }
    public static List<Path> 목록(Path wopu_a_ttaaleemüin) throws IOException {
        try (Stream<Path> ekeroliaa_ajutuu = Files.list(wopu_a_ttaaleemüin)) { return ekeroliaa_ajutuu.sorted().collect(Collectors.toList()); }
    }
}
