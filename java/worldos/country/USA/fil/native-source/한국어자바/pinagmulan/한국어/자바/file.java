// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 file 도우미. */
public final class file {
    private file() {}
    public static Path path(String pangalan) { return Path.of(pangalan); }
    public static String 읽기(Path path) throws IOException {
        return Files.readString(path, StandardCharsets.UTF_8);
    }
    public static Path sumulat(Path path, String Nilalaman_VALUE) throws IOException {
        return Files.writeString(path, Nilalaman_VALUE, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path path) throws IOException { return Files.readAllBytes(path); }
    public static Path sumulat_byte_VALUE(Path path, byte[] Nilalaman_VALUE) throws IOException { return Files.write(path, Nilalaman_VALUE); }
    public static Path Create_Directory(Path path) throws IOException { return Files.createDirectories(path); }
    public static boolean 있는가(Path path) { return Files.exists(path); }
    public static boolean burahin_pagpasok(Path path) throws IOException { return Files.deleteIfExists(path); }
    public static List<Path> pagpasok_list(Path path) throws IOException {
        try (Stream<Path> pagpasok_VALUE = Files.list(path)) { return pagpasok_VALUE.sorted().collect(Collectors.toList()); }
    }
}
