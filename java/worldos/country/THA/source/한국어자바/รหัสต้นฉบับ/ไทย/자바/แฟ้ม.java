// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ไทย.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 แฟ้ม 도우미. */
public final class แฟ้ม {
    private แฟ้ม() {}
    public static Path เส้นทาง(String ชื่อ) { return Path.of(ชื่อ); }
    public static String อ่าน(Path เส้นทาง) throws IOException {
        return Files.readString(เส้นทาง, StandardCharsets.UTF_8);
    }
    public static Path เขียน(Path เส้นทาง, String เนื้อหา_ค่า) throws IOException {
        return Files.writeString(เส้นทาง, เนื้อหา_ค่า, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path เส้นทาง) throws IOException { return Files.readAllBytes(เส้นทาง); }
    public static Path 바이트쓰기(Path เส้นทาง, byte[] เนื้อหา_ค่า) throws IOException { return Files.write(เส้นทาง, เนื้อหา_ค่า); }
    public static Path เปิด_ไดเรกทอรี(Path เส้นทาง) throws IOException { return Files.createDirectories(เส้นทาง); }
    public static boolean 있는가(Path เส้นทาง) { return Files.exists(เส้นทาง); }
    public static boolean ลบ_รายการ(Path เส้นทาง) throws IOException { return Files.deleteIfExists(เส้นทาง); }
    public static List<Path> รายการ_รายการ(Path เส้นทาง) throws IOException {
        try (Stream<Path> รายการ_ค่า = Files.list(เส้นทาง)) { return รายการ_ค่า.sorted().collect(Collectors.toList()); }
    }
}
