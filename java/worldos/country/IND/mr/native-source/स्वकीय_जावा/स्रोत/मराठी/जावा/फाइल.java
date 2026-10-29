// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package मराठी.जावा;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** प्रमाणित Path आणि IOException थेट वापरणारे UTF-8 संचिका साहाय्यक. */
public final class फाइल {
    private फाइल() {}
    public static Path मार्ग(String नाव) { return Path.of(नाव); }
    public static String वाचन(Path मार्ग) throws IOException {
        return Files.readString(मार्ग, StandardCharsets.UTF_8);
    }
    public static Path लेखन(Path मार्ग, String सामुग्री_मूल्य) throws IOException {
        return Files.writeString(मार्ग, सामुग्री_मूल्य, StandardCharsets.UTF_8);
    }
    public static byte[] बाइट_मूल्य_वाचा(Path मार्ग) throws IOException { return Files.readAllBytes(मार्ग); }
    public static Path बाइट_मूल्य_लिहा(Path मार्ग, byte[] सामुग्री_मूल्य) throws IOException { return Files.write(मार्ग, सामुग्री_मूल्य); }
    public static Path निर्देशिका_तयार_करा(Path मार्ग) throws IOException { return Files.createDirectories(मार्ग); }
    public static boolean करते_अस्तित्व(Path मार्ग) { return Files.exists(मार्ग); }
    public static boolean पुसा_प्रविष्टी(Path मार्ग) throws IOException { return Files.deleteIfExists(मार्ग); }
    public static List<Path> प्रविष्टी_यादी(Path मार्ग) throws IOException {
        try (Stream<Path> प्रविष्टी_मूल्य = Files.list(मार्ग)) { return प्रविष्टी_मूल्य.sorted().collect(Collectors.toList()); }
    }
}
