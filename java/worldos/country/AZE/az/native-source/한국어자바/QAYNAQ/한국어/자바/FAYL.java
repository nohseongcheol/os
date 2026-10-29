// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 FAYL 도우미. */
public final class FAYL {
    private FAYL() {}
    public static Path Cığır(String Ad) { return Path.of(Ad); }
    public static String Oxuma(Path Cığır) throws IOException {
        return Files.readString(Cığır, StandardCharsets.UTF_8);
    }
    public static Path Yazma(Path Cığır, String Məzmun_VALUE) throws IOException {
        return Files.writeString(Cığır, Məzmun_VALUE, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path Cığır) throws IOException { return Files.readAllBytes(Cığır); }
    public static Path yazmaq_bayt_VALUE(Path Cığır, byte[] Məzmun_VALUE) throws IOException { return Files.write(Cığır, Məzmun_VALUE); }
    public static Path yarat_kataloq(Path Cığır) throws IOException { return Files.createDirectories(Cığır); }
    public static boolean 있는가(Path Cığır) { return Files.exists(Cığır); }
    public static boolean silmək_daxiletmə_c8dbc399(Path Cığır) throws IOException { return Files.deleteIfExists(Cığır); }
    public static List<Path> daxiletmə_Siyahı(Path Cığır) throws IOException {
        try (Stream<Path> daxiletmə_VALUE = Files.list(Cığır)) { return daxiletmə_VALUE.sorted().collect(Collectors.toList()); }
    }
}
