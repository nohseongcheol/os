// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package اردو.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 فائل_کا_نام 도우미. */
public final class فائل_کا_نام {
    private فائل_کا_نام() {}
    public static Path راستہ_2(String نام) { return Path.of(نام); }
    public static String پڑھیں(Path راستہ_2) throws IOException {
        return Files.readString(راستہ_2, StandardCharsets.UTF_8);
    }
    public static Path لکھیں(Path راستہ_2, String مشمول_قدر) throws IOException {
        return Files.writeString(راستہ_2, مشمول_قدر, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path راستہ_2) throws IOException { return Files.readAllBytes(راستہ_2); }
    public static Path لکھیں_بائٹ_قدر(Path راستہ_2, byte[] مشمول_قدر) throws IOException { return Files.write(راستہ_2, مشمول_قدر); }
    public static Path بنائیں_ڈائریکٹری(Path راستہ_2) throws IOException { return Files.createDirectories(راستہ_2); }
    public static boolean 있는가(Path راستہ_2) { return Files.exists(راستہ_2); }
    public static boolean 지우기(Path راستہ_2) throws IOException { return Files.deleteIfExists(راستہ_2); }
    public static List<Path> اندراج_فہرست(Path راستہ_2) throws IOException {
        try (Stream<Path> اندراج_قدر = Files.list(راستہ_2)) { return اندراج_قدر.sorted().collect(Collectors.toList()); }
    }
}
