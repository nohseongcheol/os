// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 Faịlụ 도우미. */
public final class Faịlụ {
    private Faịlụ() {}
    public static Path ụzọ_ozi(String Aha) { return Path.of(Aha); }
    public static String Wepụta_ọzi(Path ụzọ_ozi) throws IOException {
        return Files.readString(ụzọ_ozi, StandardCharsets.UTF_8);
    }
    public static Path Chekwaa_ozi(Path ụzọ_ozi, String ndịnà_valuu) throws IOException {
        return Files.writeString(ụzọ_ozi, ndịnà_valuu, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path ụzọ_ozi) throws IOException { return Files.readAllBytes(ụzọ_ozi); }
    public static Path dee_baịtị_valuu(Path ụzọ_ozi, byte[] ndịnà_valuu) throws IOException { return Files.write(ụzọ_ozi, ndịnà_valuu); }
    public static Path mepụta_dàịrektrị(Path ụzọ_ozi) throws IOException { return Files.createDirectories(ụzọ_ozi); }
    public static boolean 있는가(Path ụzọ_ozi) { return Files.exists(ụzọ_ozi); }
    public static boolean 지우기(Path ụzọ_ozi) throws IOException { return Files.deleteIfExists(ụzọ_ozi); }
    public static List<Path> ndebà_ndepụta(Path ụzọ_ozi) throws IOException {
        try (Stream<Path> ndebà_valuu = Files.list(ụzọ_ozi)) { return ndebà_valuu.sorted().collect(Collectors.toList()); }
    }
}
