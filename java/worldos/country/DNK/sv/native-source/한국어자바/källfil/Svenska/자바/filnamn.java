// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Svenska.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 filnamn hjälpkomponent_värde. */
public final class filnamn {
    private filnamn() {}
    public static Path sökväg_2(String Namn) { return Path.of(Namn); }
    public static String Läs(Path sökväg_2) throws IOException {
        return Files.readString(sökväg_2, StandardCharsets.UTF_8);
    }
    public static Path Skriv(Path sökväg_2, String Innehåll_värde) throws IOException {
        return Files.writeString(sökväg_2, Innehåll_värde, StandardCharsets.UTF_8);
    }
    public static byte[] läsa_byte_värde(Path sökväg_2) throws IOException { return Files.readAllBytes(sökväg_2); }
    public static Path skriva_byte_värde(Path sökväg_2, byte[] Innehåll_värde) throws IOException { return Files.write(sökväg_2, Innehåll_värde); }
    public static Path Skapa_Katalog(Path sökväg_2) throws IOException { return Files.createDirectories(sökväg_2); }
    public static boolean 있는가(Path sökväg_2) { return Files.exists(sökväg_2); }
    public static boolean radera_post(Path sökväg_2) throws IOException { return Files.deleteIfExists(sökväg_2); }
    public static List<Path> post_ange(Path sökväg_2) throws IOException {
        try (Stream<Path> post_värde = Files.list(sökväg_2)) { return post_värde.sorted().collect(Collectors.toList()); }
    }
}
