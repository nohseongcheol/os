// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package فارسی.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 پرونده 도우미. */
public final class پرونده {
    private پرونده() {}
    public static Path مسیر(String نام) { return Path.of(نام); }
    public static String خواندن(Path مسیر) throws IOException {
        return Files.readString(مسیر, StandardCharsets.UTF_8);
    }
    public static Path نوشتن(Path مسیر, String محتوا_مقدار) throws IOException {
        return Files.writeString(مسیر, محتوا_مقدار, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path مسیر) throws IOException { return Files.readAllBytes(مسیر); }
    public static Path نوشتن_بایت_مقدار(Path مسیر, byte[] محتوا_مقدار) throws IOException { return Files.write(مسیر, محتوا_مقدار); }
    public static Path ایجاد_فهرست(Path مسیر) throws IOException { return Files.createDirectories(مسیر); }
    public static boolean 있는가(Path مسیر) { return Files.exists(مسیر); }
    public static boolean پاک_کردن_ورودی(Path مسیر) throws IOException { return Files.deleteIfExists(مسیر); }
    public static List<Path> ورودی_لیست(Path مسیر) throws IOException {
        try (Stream<Path> ورودی_مقدار = Files.list(مسیر)) { return ورودی_مقدار.sorted().collect(Collectors.toList()); }
    }
}
