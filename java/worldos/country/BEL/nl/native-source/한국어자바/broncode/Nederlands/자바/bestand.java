// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nederlands.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 bestand helper_WAARDE. */
public final class bestand {
    private bestand() {}
    public static Path pad(String Naam) { return Path.of(Naam); }
    public static String Lezen(Path pad) throws IOException {
        return Files.readString(pad, StandardCharsets.UTF_8);
    }
    public static Path Schrijven(Path pad, String Inhoud_WAARDE) throws IOException {
        return Files.writeString(pad, Inhoud_WAARDE, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path pad) throws IOException { return Files.readAllBytes(pad); }
    public static Path schrijven_byte_WAARDE(Path pad, byte[] Inhoud_WAARDE) throws IOException { return Files.write(pad, Inhoud_WAARDE); }
    public static Path maken_map(Path pad) throws IOException { return Files.createDirectories(pad); }
    public static boolean 있는가(Path pad) { return Files.exists(pad); }
    public static boolean wissen_invoer(Path pad) throws IOException { return Files.deleteIfExists(pad); }
    public static List<Path> invoer_Lijst_f07b3200(Path pad) throws IOException {
        try (Stream<Path> invoer_WAARDE_962f286b = Files.list(pad)) { return invoer_WAARDE_962f286b.sorted().collect(Collectors.toList()); }
    }
}
