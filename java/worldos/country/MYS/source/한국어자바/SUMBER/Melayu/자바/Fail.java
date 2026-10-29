// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Melayu.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 Fail 도우미. */
public final class Fail {
    private Fail() {}
    public static Path LALUAN(String Nama) { return Path.of(Nama); }
    public static String Baca(Path LALUAN) throws IOException {
        return Files.readString(LALUAN, StandardCharsets.UTF_8);
    }
    public static Path Tulis(Path LALUAN, String Kandungan_VALUE) throws IOException {
        return Files.writeString(LALUAN, Kandungan_VALUE, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path LALUAN) throws IOException { return Files.readAllBytes(LALUAN); }
    public static Path tulis_bait_VALUE(Path LALUAN, byte[] Kandungan_VALUE) throws IOException { return Files.write(LALUAN, Kandungan_VALUE); }
    public static Path cipta_direktori(Path LALUAN) throws IOException { return Files.createDirectories(LALUAN); }
    public static boolean 있는가(Path LALUAN) { return Files.exists(LALUAN); }
    public static boolean padam_pemasukan(Path LALUAN) throws IOException { return Files.deleteIfExists(LALUAN); }
    public static List<Path> pemasukan_Senarai(Path LALUAN) throws IOException {
        try (Stream<Path> pemasukan_VALUE = Files.list(LALUAN)) { return pemasukan_VALUE.sorted().collect(Collectors.toList()); }
    }
}
