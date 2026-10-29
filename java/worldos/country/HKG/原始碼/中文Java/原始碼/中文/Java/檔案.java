// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.Java;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 直接使用標準 Path 與 IOException 的 UTF-8 檔案輔助工具。 */
public final class 檔案 {
    private 檔案() {}
    public static Path 路徑(String 名稱) { return Path.of(名稱); }
    public static String 讀取(Path 路徑) throws IOException {
        return Files.readString(路徑, StandardCharsets.UTF_8);
    }
    public static Path 寫入(Path 路徑, String 內容值) throws IOException {
        return Files.writeString(路徑, 內容值, StandardCharsets.UTF_8);
    }
    public static byte[] 讀取位元組值(Path 路徑) throws IOException { return Files.readAllBytes(路徑); }
    public static Path 寫入位元組值(Path 路徑, byte[] 內容值) throws IOException { return Files.write(路徑, 內容值); }
    public static Path 創建目錄(Path 路徑) throws IOException { return Files.createDirectories(路徑); }
    public static boolean 是否執行存在(Path 路徑) { return Files.exists(路徑); }
    public static boolean 擦除條目(Path 路徑) throws IOException { return Files.deleteIfExists(路徑); }
    public static List<Path> 條目列表(Path 路徑) throws IOException {
        try (Stream<Path> 條目值 = Files.list(路徑)) { return 條目值.sorted().collect(Collectors.toList()); }
    }
}
