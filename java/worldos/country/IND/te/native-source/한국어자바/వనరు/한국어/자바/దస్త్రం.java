// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 దస్త్రం 도우미. */
public final class దస్త్రం {
    private దస్త్రం() {}
    public static Path పాత్(String పేరు) { return Path.of(పేరు); }
    public static String చదువు(Path పాత్) throws IOException {
        return Files.readString(పాత్, StandardCharsets.UTF_8);
    }
    public static Path వ్రాయుము(Path పాత్, String విషయం_మూల్యం) throws IOException {
        return Files.writeString(పాత్, విషయం_మూల్యం, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path పాత్) throws IOException { return Files.readAllBytes(పాత్); }
    public static Path వ్రాయి_బైట్_మూల్యం(Path పాత్, byte[] విషయం_మూల్యం) throws IOException { return Files.write(పాత్, విషయం_మూల్యం); }
    public static Path క్రియేట్_సంచయని(Path పాత్) throws IOException { return Files.createDirectories(పాత్); }
    public static boolean 있는가(Path పాత్) { return Files.exists(పాత్); }
    public static boolean తుడిచివేయి_ప్రవేశం(Path పాత్) throws IOException { return Files.deleteIfExists(పాత్); }
    public static List<Path> ప్రవేశం_జాబితా(Path పాత్) throws IOException {
        try (Stream<Path> ప్రవేశం_మూల్యం = Files.list(పాత్)) { return ప్రవేశం_మూల్యం.sorted().collect(Collectors.toList()); }
    }
}
