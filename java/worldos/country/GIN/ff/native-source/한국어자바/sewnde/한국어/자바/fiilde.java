// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 fiilde 도우미. */
public final class fiilde {
    private fiilde() {}
    public static Path laawol(String innde) { return Path.of(innde); }
    public static String 읽기(Path laawol) throws IOException {
        return Files.readString(laawol, StandardCharsets.UTF_8);
    }
    public static Path winndude(Path laawol, String loowdi_njaru) throws IOException {
        return Files.writeString(laawol, loowdi_njaru, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path laawol) throws IOException { return Files.readAllBytes(laawol); }
    public static Path winndude_oktee_njaru(Path laawol, byte[] loowdi_njaru) throws IOException { return Files.write(laawol, loowdi_njaru); }
    public static Path 폴더만들기(Path laawol) throws IOException { return Files.createDirectories(laawol); }
    public static boolean 있는가(Path laawol) { return Files.exists(laawol); }
    public static boolean 지우기(Path laawol) throws IOException { return Files.deleteIfExists(laawol); }
    public static List<Path> naatnugol_Doggol(Path laawol) throws IOException {
        try (Stream<Path> naatnugol_njaru = Files.list(laawol)) { return naatnugol_njaru.sorted().collect(Collectors.toList()); }
    }
}
