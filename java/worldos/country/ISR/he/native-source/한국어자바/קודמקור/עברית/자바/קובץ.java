// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package עברית.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 קובץ עוזר_ערך. */
public final class קובץ {
    private קובץ() {}
    public static Path נתיב(String שם) { return Path.of(שם); }
    public static String קרא(Path נתיב) throws IOException {
        return Files.readString(נתיב, StandardCharsets.UTF_8);
    }
    public static Path כתוב(Path נתיב, String תוכן_ערך) throws IOException {
        return Files.writeString(נתיב, תוכן_ערך, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path נתיב) throws IOException { return Files.readAllBytes(נתיב); }
    public static Path כתיבה_בית_ערך(Path נתיב, byte[] תוכן_ערך) throws IOException { return Files.write(נתיב, תוכן_ערך); }
    public static Path ליצור_מדריך(Path נתיב) throws IOException { return Files.createDirectories(נתיב); }
    public static boolean 있는가(Path נתיב) { return Files.exists(נתיב); }
    public static boolean מחק_ערך(Path נתיב) throws IOException { return Files.deleteIfExists(נתיב); }
    public static List<Path> ערך_רשימה(Path נתיב) throws IOException {
        try (Stream<Path> ערך_ערך = Files.list(נתיב)) { return ערך_ערך.sorted().collect(Collectors.toList()); }
    }
}
