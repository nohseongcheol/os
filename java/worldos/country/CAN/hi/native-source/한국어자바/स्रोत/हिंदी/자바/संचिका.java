// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package हिंदी.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 संचिका 도우미. */
public final class संचिका {
    private संचिका() {}
    public static Path पथ(String नाम) { return Path.of(नाम); }
    public static String पढ़ें(Path पथ) throws IOException {
        return Files.readString(पथ, StandardCharsets.UTF_8);
    }
    public static Path लिखें(Path पथ, String सामग्री_मान) throws IOException {
        return Files.writeString(पथ, सामग्री_मान, StandardCharsets.UTF_8);
    }
    public static byte[] पढें_बाइट_मान(Path पथ) throws IOException { return Files.readAllBytes(पथ); }
    public static Path लिखना_बाइट_मान(Path पथ, byte[] सामग्री_मान) throws IOException { return Files.write(पथ, सामग्री_मान); }
    public static Path बनाएँ_डायरेक्टरी(Path पथ) throws IOException { return Files.createDirectories(पथ); }
    public static boolean 있는가(Path पथ) { return Files.exists(पथ); }
    public static boolean मिटाएँ_एन्ट्री(Path पथ) throws IOException { return Files.deleteIfExists(पथ); }
    public static List<Path> एन्ट्री_सूची(Path पथ) throws IOException {
        try (Stream<Path> एन्ट्री_मान = Files.list(पथ)) { return एन्ट्री_मान.sorted().collect(Collectors.toList()); }
    }
}
