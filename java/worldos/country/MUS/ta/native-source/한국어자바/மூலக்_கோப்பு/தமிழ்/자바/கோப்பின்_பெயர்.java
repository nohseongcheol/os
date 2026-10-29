// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package தமிழ்.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 கோப்பின்_பெயர் 도우미. */
public final class கோப்பின்_பெயர் {
    private கோப்பின்_பெயர்() {}
    public static Path பாதை_2(String பெயர்) { return Path.of(பெயர்); }
    public static String படி(Path பாதை_2) throws IOException {
        return Files.readString(பாதை_2, StandardCharsets.UTF_8);
    }
    public static Path எழுது(Path பாதை_2, String உள்ளடக்கம்_மதிப்பு) throws IOException {
        return Files.writeString(பாதை_2, உள்ளடக்கம்_மதிப்பு, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path பாதை_2) throws IOException { return Files.readAllBytes(பாதை_2); }
    public static Path எழுது_பைட்_மதிப்பு(Path பாதை_2, byte[] உள்ளடக்கம்_மதிப்பு) throws IOException { return Files.write(பாதை_2, உள்ளடக்கம்_மதிப்பு); }
    public static Path உருவாக்கு_கோப்பகம்(Path பாதை_2) throws IOException { return Files.createDirectories(பாதை_2); }
    public static boolean 있는가(Path பாதை_2) { return Files.exists(பாதை_2); }
    public static boolean அழி_உள்ளீடு(Path பாதை_2) throws IOException { return Files.deleteIfExists(பாதை_2); }
    public static List<Path> உள்ளீடு_பட்டியல்(Path பாதை_2) throws IOException {
        try (Stream<Path> உள்ளீடு_மதிப்பு = Files.list(பாதை_2)) { return உள்ளீடு_மதிப்பு.sorted().collect(Collectors.toList()); }
    }
}
