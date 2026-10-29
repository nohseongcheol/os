// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package বাংলা.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 নথির_নাম 도우미. */
public final class নথির_নাম {
    private নথির_নাম() {}
    public static Path পথ_2(String নাম) { return Path.of(নাম); }
    public static String পড়া(Path পথ_2) throws IOException {
        return Files.readString(পথ_2, StandardCharsets.UTF_8);
    }
    public static Path লেখা(Path পথ_2, String সামগ্রি_মান) throws IOException {
        return Files.writeString(পথ_2, সামগ্রি_মান, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path পথ_2) throws IOException { return Files.readAllBytes(পথ_2); }
    public static Path লেখা_বাইট_মান(Path পথ_2, byte[] সামগ্রি_মান) throws IOException { return Files.write(পথ_2, সামগ্রি_মান); }
    public static Path ক্রিয়েট_ডিরেক্টরি(Path পথ_2) throws IOException { return Files.createDirectories(পথ_2); }
    public static boolean 있는가(Path পথ_2) { return Files.exists(পথ_2); }
    public static boolean মুছুন_ভুক্তি(Path পথ_2) throws IOException { return Files.deleteIfExists(পথ_2); }
    public static List<Path> ভুক্তি_তালিকা(Path পথ_2) throws IOException {
        try (Stream<Path> ভুক্তি_মান = Files.list(পথ_2)) { return ভুক্তি_মান.sorted().collect(Collectors.toList()); }
    }
}
