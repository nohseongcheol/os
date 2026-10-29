// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 ଫାଇଲ 도우미. */
public final class ଫାଇଲ {
    private ଫାଇଲ() {}
    public static Path ପଥ(String ନାମ) { return Path.of(ନାମ); }
    public static String ପଢନ୍ତୁ(Path ପଥ) throws IOException {
        return Files.readString(ପଥ, StandardCharsets.UTF_8);
    }
    public static Path ଲେଖନ୍ତୁ(Path ପଥ, String ବିଷୟ_ମୂଲ୍ୟ) throws IOException {
        return Files.writeString(ପଥ, ବିଷୟ_ମୂଲ୍ୟ, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path ପଥ) throws IOException { return Files.readAllBytes(ପଥ); }
    public static Path ଲିଖନ_ବାଇଟ୍_ମୂଲ୍ୟ(Path ପଥ, byte[] ବିଷୟ_ମୂଲ୍ୟ) throws IOException { return Files.write(ପଥ, ବିଷୟ_ମୂଲ୍ୟ); }
    public static Path ସୃଷ୍ଟି_ଡିରେକ୍ଟୋରୀ(Path ପଥ) throws IOException { return Files.createDirectories(ପଥ); }
    public static boolean 있는가(Path ପଥ) { return Files.exists(ପଥ); }
    public static boolean 지우기(Path ପଥ) throws IOException { return Files.deleteIfExists(ପଥ); }
    public static List<Path> ଏଣ୍ଟ୍ରି_ତାଲିକା(Path ପଥ) throws IOException {
        try (Stream<Path> ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ = Files.list(ପଥ)) { return ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.sorted().collect(Collectors.toList()); }
    }
}
