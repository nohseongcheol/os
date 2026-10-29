// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 دوتنه 도우미. */
public final class دوتنه {
    private دوتنه() {}
    public static Path يونلور(String نوم) { return Path.of(نوم); }
    public static String لوستل(Path يونلور) throws IOException {
        return Files.readString(يونلور, StandardCharsets.UTF_8);
    }
    public static Path لوستل_2(Path يونلور, String منځپانګه_ارزښت) throws IOException {
        return Files.writeString(يونلور, منځپانګه_ارزښت, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path يونلور) throws IOException { return Files.readAllBytes(يونلور); }
    public static Path ليکل_بايټ_ارزښت(Path يونلور, byte[] منځپانګه_ارزښت) throws IOException { return Files.write(يونلور, منځپانګه_ارزښت); }
    public static Path 폴더만들기(Path يونلور) throws IOException { return Files.createDirectories(يونلور); }
    public static boolean 있는가(Path يونلور) { return Files.exists(يونلور); }
    public static boolean 지우기(Path يونلور) throws IOException { return Files.deleteIfExists(يونلور); }
    public static List<Path> 목록(Path يونلور) throws IOException {
        try (Stream<Path> ننوت_ارزښت = Files.list(يونلور)) { return ننوت_ارزښت.sorted().collect(Collectors.toList()); }
    }
}
