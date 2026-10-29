// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 bara_denc 도우미. */
public final class bara_denc {
    private bara_denc() {}
    public static Path Yoonu_jëmale(String tur_253d1510) { return Path.of(tur_253d1510); }
    public static String 읽기(Path Yoonu_jëmale) throws IOException {
        return Files.readString(Yoonu_jëmale, StandardCharsets.UTF_8);
    }
    public static Path biir(Path Yoonu_jëmale, String Këmb_xëyma) throws IOException {
        return Files.writeString(Yoonu_jëmale, Këmb_xëyma, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path Yoonu_jëmale) throws IOException { return Files.readAllBytes(Yoonu_jëmale); }
    public static Path biir_okte_xëyma(Path Yoonu_jëmale, byte[] Këmb_xëyma) throws IOException { return Files.write(Yoonu_jëmale, Këmb_xëyma); }
    public static Path sos_dàmb(Path Yoonu_jëmale) throws IOException { return Files.createDirectories(Yoonu_jëmale); }
    public static boolean 있는가(Path Yoonu_jëmale) { return Files.exists(Yoonu_jëmale); }
    public static boolean 지우기(Path Yoonu_jëmale) throws IOException { return Files.deleteIfExists(Yoonu_jëmale); }
    public static List<Path> dugal_xabaar_lim(Path Yoonu_jëmale) throws IOException {
        try (Stream<Path> dugal_xabaar_xëyma = Files.list(Yoonu_jëmale)) { return dugal_xabaar_xëyma.sorted().collect(Collectors.toList()); }
    }
}
