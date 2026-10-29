// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 ឯកសារ 도우미. */
public final class ឯកសារ {
    private ឯកសារ() {}
    public static Path ផ្លូវ(String ឈ្មោះ) { return Path.of(ឈ្មោះ); }
    public static String អាន(Path ផ្លូវ) throws IOException {
        return Files.readString(ផ្លូវ, StandardCharsets.UTF_8);
    }
    public static Path សរសេរ(Path ផ្លូវ, String មាតិកា_តំលៃ) throws IOException {
        return Files.writeString(ផ្លូវ, មាតិកា_តំលៃ, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path ផ្លូវ) throws IOException { return Files.readAllBytes(ផ្លូវ); }
    public static Path សរសេរ_បៃ_តំលៃ(Path ផ្លូវ, byte[] មាតិកា_តំលៃ) throws IOException { return Files.write(ផ្លូវ, មាតិកា_តំលៃ); }
    public static Path បង្កើត_បញ្ជី(Path ផ្លូវ) throws IOException { return Files.createDirectories(ផ្លូវ); }
    public static boolean 있는가(Path ផ្លូវ) { return Files.exists(ផ្លូវ); }
    public static boolean លុប_ការបញ្ចូល(Path ផ្លូវ) throws IOException { return Files.deleteIfExists(ផ្លូវ); }
    public static List<Path> ការបញ្ចូល_បញ្ជី(Path ផ្លូវ) throws IOException {
        try (Stream<Path> ការបញ្ចូល_តំលៃ = Files.list(ផ្លូវ)) { return ការបញ្ចូល_តំលៃ.sorted().collect(Collectors.toList()); }
    }
}
