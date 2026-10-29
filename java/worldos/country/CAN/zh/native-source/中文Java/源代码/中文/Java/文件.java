// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.Java;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 直接使用标准 Path 和 IOException 的 UTF-8 文件辅助工具。 */
public final class 文件 {
    private 文件() {}
    public static Path 路径(String 名称) { return Path.of(名称); }
    public static String 读取(Path 路径) throws IOException {
        return Files.readString(路径, StandardCharsets.UTF_8);
    }
    public static Path 写入(Path 路径, String 内容值) throws IOException {
        return Files.writeString(路径, 内容值, StandardCharsets.UTF_8);
    }
    public static byte[] 读取字节值(Path 路径) throws IOException { return Files.readAllBytes(路径); }
    public static Path 写入字节值(Path 路径, byte[] 内容值) throws IOException { return Files.write(路径, 内容值); }
    public static Path 创建目录(Path 路径) throws IOException { return Files.createDirectories(路径); }
    public static boolean 是否执行存在(Path 路径) { return Files.exists(路径); }
    public static boolean 擦除条目(Path 路径) throws IOException { return Files.deleteIfExists(路径); }
    public static List<Path> 条目列表(Path 路径) throws IOException {
        try (Stream<Path> 条目值 = Files.list(路径)) { return 条目值.sorted().collect(Collectors.toList()); }
    }
}
