// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 Fáìlì 도우미. */
public final class Fáìlì {
    private Fáìlì() {}
    public static Path ọ̀nà(String Orúkọ) { return Path.of(Orúkọ); }
    public static String Kàá(Path ọ̀nà) throws IOException {
        return Files.readString(ọ̀nà, StandardCharsets.UTF_8);
    }
    public static Path Kọ(Path ọ̀nà, String Àkóónú_iye) throws IOException {
        return Files.writeString(ọ̀nà, Àkóónú_iye, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path ọ̀nà) throws IOException { return Files.readAllBytes(ọ̀nà); }
    public static Path kọ_báìtì_iye(Path ọ̀nà, byte[] Àkóónú_iye) throws IOException { return Files.write(ọ̀nà, Àkóónú_iye); }
    public static Path Ṣẹ̀dá_àkójọpọ̀_fáìlì(Path ọ̀nà) throws IOException { return Files.createDirectories(ọ̀nà); }
    public static boolean 있는가(Path ọ̀nà) { return Files.exists(ọ̀nà); }
    public static boolean 지우기(Path ọ̀nà) throws IOException { return Files.deleteIfExists(ọ̀nà); }
    public static List<Path> ìgbéwọlé_Àtòkọ(Path ọ̀nà) throws IOException {
        try (Stream<Path> ìgbéwọlé_iye = Files.list(ọ̀nà)) { return ìgbéwọlé_iye.sorted().collect(Collectors.toList()); }
    }
}
