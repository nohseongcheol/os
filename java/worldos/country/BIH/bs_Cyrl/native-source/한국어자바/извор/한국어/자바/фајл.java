// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 фајл 도우미. */
public final class фајл {
    private фајл() {}
    public static Path пут(String назив) { return Path.of(назив); }
    public static String 읽기(Path пут) throws IOException {
        return Files.readString(пут, StandardCharsets.UTF_8);
    }
    public static Path писати(Path пут, String Садржај_вриједност) throws IOException {
        return Files.writeString(пут, Садржај_вриједност, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path пут) throws IOException { return Files.readAllBytes(пут); }
    public static Path писати_бајт_вриједност(Path пут, byte[] Садржај_вриједност) throws IOException { return Files.write(пут, Садржај_вриједност); }
    public static Path 폴더만들기(Path пут) throws IOException { return Files.createDirectories(пут); }
    public static boolean 있는가(Path пут) { return Files.exists(пут); }
    public static boolean 지우기(Path пут) throws IOException { return Files.deleteIfExists(пут); }
    public static List<Path> унос_списак(Path пут) throws IOException {
        try (Stream<Path> унос_вриједност = Files.list(пут)) { return унос_вриједност.sorted().collect(Collectors.toList()); }
    }
}
