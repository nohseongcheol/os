// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 日本語.Java;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 標準 Path と IOException をそのまま使う UTF-8 ファイル補助機能。 */
public final class ファイル {
    private ファイル() {}
    public static Path 経路(String 名前) { return Path.of(名前); }
    public static String 読取(Path 経路) throws IOException {
        return Files.readString(経路, StandardCharsets.UTF_8);
    }
    public static Path 書込(Path 経路, String 内容物値) throws IOException {
        return Files.writeString(経路, 内容物値, StandardCharsets.UTF_8);
    }
    public static byte[] バイト値読取(Path 経路) throws IOException { return Files.readAllBytes(経路); }
    public static Path バイト値書込(Path 経路, byte[] 内容物値) throws IOException { return Files.write(経路, 内容物値); }
    public static Path ディレクトリ作成(Path 経路) throws IOException { return Files.createDirectories(経路); }
    public static boolean 実施判定存在(Path 経路) { return Files.exists(経路); }
    public static boolean 入口消去処理(Path 経路) throws IOException { return Files.deleteIfExists(経路); }
    public static List<Path> 入口一覧(Path 経路) throws IOException {
        try (Stream<Path> 入口値 = Files.list(経路)) { return 入口値.sorted().collect(Collectors.toList()); }
    }
}
