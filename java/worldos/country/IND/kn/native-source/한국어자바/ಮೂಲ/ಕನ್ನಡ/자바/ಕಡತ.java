// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ಕನ್ನಡ.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 ಕಡತ 도우미. */
public final class ಕಡತ {
    private ಕಡತ() {}
    public static Path ಮಾರ್ಗ(String ಹೆಸರು) { return Path.of(ಹೆಸರು); }
    public static String ಓದು(Path ಮಾರ್ಗ) throws IOException {
        return Files.readString(ಮಾರ್ಗ, StandardCharsets.UTF_8);
    }
    public static Path ಬರೆ(Path ಮಾರ್ಗ, String ವಿಷಯ_ಮೌಲ್ಯ) throws IOException {
        return Files.writeString(ಮಾರ್ಗ, ವಿಷಯ_ಮೌಲ್ಯ, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path ಮಾರ್ಗ) throws IOException { return Files.readAllBytes(ಮಾರ್ಗ); }
    public static Path ಬರೆ_ಬೈಟ್_ಮೌಲ್ಯ(Path ಮಾರ್ಗ, byte[] ವಿಷಯ_ಮೌಲ್ಯ) throws IOException { return Files.write(ಮಾರ್ಗ, ವಿಷಯ_ಮೌಲ್ಯ); }
    public static Path ರಚಿಸು_ಡೈರೆಕ್ಟರಿ(Path ಮಾರ್ಗ) throws IOException { return Files.createDirectories(ಮಾರ್ಗ); }
    public static boolean 있는가(Path ಮಾರ್ಗ) { return Files.exists(ಮಾರ್ಗ); }
    public static boolean ಅಳಿಸು_ನಮೂದು(Path ಮಾರ್ಗ) throws IOException { return Files.deleteIfExists(ಮಾರ್ಗ); }
    public static List<Path> ನಮೂದು_ಪಟ್ಟಿ(Path ಮಾರ್ಗ) throws IOException {
        try (Stream<Path> ನಮೂದು_ಮೌಲ್ಯ = Files.list(ಮಾರ್ಗ)) { return ನಮೂದು_ಮೌಲ್ಯ.sorted().collect(Collectors.toList()); }
    }
}
