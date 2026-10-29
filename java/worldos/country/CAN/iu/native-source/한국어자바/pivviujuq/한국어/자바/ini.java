// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 ini 도우미. */
public final class ini {
    private ini() {}
    public static Path aqqut(String atiq) { return Path.of(atiq); }
    public static String 읽기(Path aqqut) throws IOException {
        return Files.readString(aqqut, StandardCharsets.UTF_8);
    }
    public static Path titiraq(Path aqqut, String Ilulingit_atuutilik) throws IOException {
        return Files.writeString(aqqut, Ilulingit_atuutilik, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path aqqut) throws IOException { return Files.readAllBytes(aqqut); }
    public static Path titiraq_byte_atuutilik(Path aqqut, byte[] Ilulingit_atuutilik) throws IOException { return Files.write(aqqut, Ilulingit_atuutilik); }
    public static Path 폴더만들기(Path aqqut) throws IOException { return Files.createDirectories(aqqut); }
    public static boolean 있는가(Path aqqut) { return Files.exists(aqqut); }
    public static boolean 지우기(Path aqqut) throws IOException { return Files.deleteIfExists(aqqut); }
    public static List<Path> Iliniku_Titiqpalliagaq(Path aqqut) throws IOException {
        try (Stream<Path> Iliniku_atuutilik = Files.list(aqqut)) { return Iliniku_atuutilik.sorted().collect(Collectors.toList()); }
    }
}
