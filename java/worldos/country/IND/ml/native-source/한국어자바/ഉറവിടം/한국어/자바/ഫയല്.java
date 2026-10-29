// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 ഫയല് 도우미. */
public final class ഫയല് {
    private ഫയല്() {}
    public static Path വഴി(String പേരു്) { return Path.of(പേരു്); }
    public static String വായന(Path വഴി) throws IOException {
        return Files.readString(വഴി, StandardCharsets.UTF_8);
    }
    public static Path എഴുത്തു്(Path വഴി, String ഉള്ളടക്കം_മൂല്യം) throws IOException {
        return Files.writeString(വഴി, ഉള്ളടക്കം_മൂല്യം, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path വഴി) throws IOException { return Files.readAllBytes(വഴി); }
    public static Path റൈറ്റ്_ചെയ്യുക_బైట్_മൂല്യം(Path വഴി, byte[] ഉള്ളടക്കം_മൂല്യം) throws IOException { return Files.write(വഴി, ഉള്ളടക്കം_മൂല്യം); }
    public static Path സൃഷ്_ടിക്കുക_ഡയറക്ടറി(Path വഴി) throws IOException { return Files.createDirectories(വഴി); }
    public static boolean 있는가(Path വഴി) { return Files.exists(വഴി); }
    public static boolean മായ്ക്കുക_എന്_ട്രി(Path വഴി) throws IOException { return Files.deleteIfExists(വഴി); }
    public static List<Path> എന്_ട്രി_ലിസ്റ്റ്(Path വഴി) throws IOException {
        try (Stream<Path> എന്_ട്രി_മൂല്യം = Files.list(വഴി)) { return എന്_ട്രി_മൂല്യം.sorted().collect(Collectors.toList()); }
    }
}
