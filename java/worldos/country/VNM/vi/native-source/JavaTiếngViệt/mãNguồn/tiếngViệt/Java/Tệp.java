// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package tiếngViệt.Java;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** Công cụ tệp UTF-8 dùng trực tiếp Path và IOException tiêu chuẩn. */
public final class Tệp {
    private Tệp() {}
    public static Path đườngDẫn(String tên) { return Path.of(tên); }
    public static String đọc(Path đườngDẫn) throws IOException {
        return Files.readString(đườngDẫn, StandardCharsets.UTF_8);
    }
    public static Path ghi(Path đườngDẫn, String giáTrịNộiDung) throws IOException {
        return Files.writeString(đườngDẫn, giáTrịNộiDung, StandardCharsets.UTF_8);
    }
    public static byte[] đọcGiáTrịByte(Path đườngDẫn) throws IOException { return Files.readAllBytes(đườngDẫn); }
    public static Path ghiGiáTrịByte(Path đườngDẫn, byte[] giáTrịNộiDung) throws IOException { return Files.write(đườngDẫn, giáTrịNộiDung); }
    public static Path tạoThưMục(Path đườngDẫn) throws IOException { return Files.createDirectories(đườngDẫn); }
    public static boolean thựcHiệnĐượcTồnTại(Path đườngDẫn) { return Files.exists(đườngDẫn); }
    public static boolean xóaMục(Path đườngDẫn) throws IOException { return Files.deleteIfExists(đườngDẫn); }
    public static List<Path> danhSáchMục(Path đườngDẫn) throws IOException {
        try (Stream<Path> giáTrịMục = Files.list(đườngDẫn)) { return giáTrịMục.sorted().collect(Collectors.toList()); }
    }
}
