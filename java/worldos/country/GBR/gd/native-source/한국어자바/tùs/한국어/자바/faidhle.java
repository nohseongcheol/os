// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 faidhle 도우미. */
public final class faidhle {
    private faidhle() {}
    public static Path Slighe(String Ainm) { return Path.of(Ainm); }
    public static String 읽기(Path Slighe) throws IOException {
        return Files.readString(Slighe, StandardCharsets.UTF_8);
    }
    public static Path sgrìobh(Path Slighe, String susbaint_VALUE) throws IOException {
        return Files.writeString(Slighe, susbaint_VALUE, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path Slighe) throws IOException { return Files.readAllBytes(Slighe); }
    public static Path sgrìobh_baidht_VALUE(Path Slighe, byte[] susbaint_VALUE) throws IOException { return Files.write(Slighe, susbaint_VALUE); }
    public static Path Create_eòlaire(Path Slighe) throws IOException { return Files.createDirectories(Slighe); }
    public static boolean 있는가(Path Slighe) { return Files.exists(Slighe); }
    public static boolean 지우기(Path Slighe) throws IOException { return Files.deleteIfExists(Slighe); }
    public static List<Path> cur_a_steach_Liosta(Path Slighe) throws IOException {
        try (Stream<Path> cur_a_steach_VALUE = Files.list(Slighe)) { return cur_a_steach_VALUE.sorted().collect(Collectors.toList()); }
    }
}
