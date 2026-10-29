// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 Ֆայլ 도우미. */
public final class Ֆայլ {
    private Ֆայլ() {}
    public static Path Ճանապարհ(String Անուն) { return Path.of(Անուն); }
    public static String Ընթերցում(Path Ճանապարհ) throws IOException {
        return Files.readString(Ճանապարհ, StandardCharsets.UTF_8);
    }
    public static Path Գրել(Path Ճանապարհ, String Բովանդակություն_արժեք) throws IOException {
        return Files.writeString(Ճանապարհ, Բովանդակություն_արժեք, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path Ճանապարհ) throws IOException { return Files.readAllBytes(Ճանապարհ); }
    public static Path գրել_բայթ_արժեք(Path Ճանապարհ, byte[] Բովանդակություն_արժեք) throws IOException { return Files.write(Ճանապարհ, Բովանդակություն_արժեք); }
    public static Path Կերտի_ր_գրացուցակ(Path Ճանապարհ) throws IOException { return Files.createDirectories(Ճանապարհ); }
    public static boolean 있는가(Path Ճանապարհ) { return Files.exists(Ճանապարհ); }
    public static boolean 지우기(Path Ճանապարհ) throws IOException { return Files.deleteIfExists(Ճանապարհ); }
    public static List<Path> մուտքագրում_Ցուցակ(Path Ճանապարհ) throws IOException {
        try (Stream<Path> մուտքագրում_արժեք = Files.list(Ճանապարհ)) { return մուտքագրում_արժեք.sorted().collect(Collectors.toList()); }
    }
}
