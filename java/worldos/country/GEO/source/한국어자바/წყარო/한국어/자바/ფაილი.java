// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 ფაილი 도우미. */
public final class ფაილი {
    private ფაილი() {}
    public static Path გეზი(String სახელი) { return Path.of(სახელი); }
    public static String კითხვა(Path გეზი) throws IOException {
        return Files.readString(გეზი, StandardCharsets.UTF_8);
    }
    public static Path ჩაწერა(Path გეზი, String შიგთავსი_მნიშვნელობა) throws IOException {
        return Files.writeString(გეზი, შიგთავსი_მნიშვნელობა, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path გეზი) throws IOException { return Files.readAllBytes(გეზი); }
    public static Path ჩაწერა_ბაიტი_მნიშვნელობა(Path გეზი, byte[] შიგთავსი_მნიშვნელობა) throws IOException { return Files.write(გეზი, შიგთავსი_მნიშვნელობა); }
    public static Path შექმნა_საქაღალდე(Path გეზი) throws IOException { return Files.createDirectories(გეზი); }
    public static boolean 있는가(Path გეზი) { return Files.exists(გეზი); }
    public static boolean 지우기(Path გეზი) throws IOException { return Files.deleteIfExists(გეზი); }
    public static List<Path> შენატანი_სია(Path გეზი) throws IOException {
        try (Stream<Path> შენატანი_მნიშვნელობა = Files.list(გეზი)) { return შენატანი_მნიშვნელობა.sorted().collect(Collectors.toList()); }
    }
}
