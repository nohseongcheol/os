// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 নথিপত্ৰ 도우미. */
public final class নথিপত্ৰ {
    private নথিপত্ৰ() {}
    public static Path পথ(String নাম) { return Path.of(নাম); }
    public static String পড়া(Path পথ) throws IOException {
        return Files.readString(পথ, StandardCharsets.UTF_8);
    }
    public static Path লিখা(Path পথ, String সামগ্ৰী_মান) throws IOException {
        return Files.writeString(পথ, সামগ্ৰী_মান, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path পথ) throws IOException { return Files.readAllBytes(পথ); }
    public static Path লিখক_বাইট_মান(Path পথ, byte[] সামগ্ৰী_মান) throws IOException { return Files.write(পথ, সামগ্ৰী_মান); }
    public static Path ক্ৰিয়েট_ডাইৰেক্টৰী(Path পথ) throws IOException { return Files.createDirectories(পথ); }
    public static boolean 있는가(Path পথ) { return Files.exists(পথ); }
    public static boolean 지우기(Path পথ) throws IOException { return Files.deleteIfExists(পথ); }
    public static List<Path> প্রবিষ্ট_সূচী(Path পথ) throws IOException {
        try (Stream<Path> প্রবিষ্ট_মান = Files.list(পথ)) { return প্রবিষ্ট_মান.sorted().collect(Collectors.toList()); }
    }
}
