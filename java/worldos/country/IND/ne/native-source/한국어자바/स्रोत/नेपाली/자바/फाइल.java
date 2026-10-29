// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package नेपाली.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 फाइल 도우미. */
public final class फाइल {
    private फाइल() {}
    public static Path मार्ग(String नाम) { return Path.of(नाम); }
    public static String पढनुहोस्(Path मार्ग) throws IOException {
        return Files.readString(मार्ग, StandardCharsets.UTF_8);
    }
    public static Path लेख्नुहोस्(Path मार्ग, String सामग्री_मान) throws IOException {
        return Files.writeString(मार्ग, सामग्री_मान, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path मार्ग) throws IOException { return Files.readAllBytes(मार्ग); }
    public static Path लेख्नुहोस्_बाइट_मान(Path मार्ग, byte[] सामग्री_मान) throws IOException { return Files.write(मार्ग, सामग्री_मान); }
    public static Path सिर्जना_डाइरेक्टरी(Path मार्ग) throws IOException { return Files.createDirectories(मार्ग); }
    public static boolean 있는가(Path मार्ग) { return Files.exists(मार्ग); }
    public static boolean 지우기(Path मार्ग) throws IOException { return Files.deleteIfExists(मार्ग); }
    public static List<Path> प्रविष्टि_सूची(Path मार्ग) throws IOException {
        try (Stream<Path> प्रविष्टि_मान = Files.list(मार्ग)) { return प्रविष्टि_मान.sorted().collect(Collectors.toList()); }
    }
}
