// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latviešu.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 Fails 도우미. */
public final class Fails {
    private Fails() {}
    public static Path CEĻŠ(String Nosaukums) { return Path.of(Nosaukums); }
    public static String Lasīt(Path CEĻŠ) throws IOException {
        return Files.readString(CEĻŠ, StandardCharsets.UTF_8);
    }
    public static Path Rakstīt(Path CEĻŠ, String Saturs_VALUE) throws IOException {
        return Files.writeString(CEĻŠ, Saturs_VALUE, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path CEĻŠ) throws IOException { return Files.readAllBytes(CEĻŠ); }
    public static Path rakstīšana_byte_VALUE(Path CEĻŠ, byte[] Saturs_VALUE) throws IOException { return Files.write(CEĻŠ, Saturs_VALUE); }
    public static Path atvērt_Direktorijs(Path CEĻŠ) throws IOException { return Files.createDirectories(CEĻŠ); }
    public static boolean 있는가(Path CEĻŠ) { return Files.exists(CEĻŠ); }
    public static boolean dzēst_ievade(Path CEĻŠ) throws IOException { return Files.deleteIfExists(CEĻŠ); }
    public static List<Path> ievade_Saraksts(Path CEĻŠ) throws IOException {
        try (Stream<Path> ievade_VALUE = Files.list(CEĻŠ)) { return ievade_VALUE.sorted().collect(Collectors.toList()); }
    }
}
