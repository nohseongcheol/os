// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package العربية.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 ملف مساعد_قيمة. */
public final class ملف {
    private ملف() {}
    public static Path مسار(String اسم) { return Path.of(اسم); }
    public static String قراءة(Path مسار) throws IOException {
        return Files.readString(مسار, StandardCharsets.UTF_8);
    }
    public static Path كتابة(Path مسار, String محتوى_قيمة) throws IOException {
        return Files.writeString(مسار, محتوى_قيمة, StandardCharsets.UTF_8);
    }
    public static byte[] يقرأ_بايت_قيمة(Path مسار) throws IOException { return Files.readAllBytes(مسار); }
    public static Path كتابة_بايت_قيمة(Path مسار, byte[] محتوى_قيمة) throws IOException { return Files.write(مسار, محتوى_قيمة); }
    public static Path فتح_دليل(Path مسار) throws IOException { return Files.createDirectories(مسار); }
    public static boolean 있는가(Path مسار) { return Files.exists(مسار); }
    public static boolean مسح_إدخال(Path مسار) throws IOException { return Files.deleteIfExists(مسار); }
    public static List<Path> إدخال_قائمة_f07b3200(Path مسار) throws IOException {
        try (Stream<Path> إدخال_قيمة_962f286b = Files.list(مسار)) { return إدخال_قيمة_962f286b.sorted().collect(Collectors.toList()); }
    }
}
