// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ਪੰਜਾਬੀ.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 ਫਾਇਲ 도우미. */
public final class ਫਾਇਲ {
    private ਫਾਇਲ() {}
    public static Path ਮਾਰਗ(String ਨਾਂ) { return Path.of(ਨਾਂ); }
    public static String ਪੜ੍ਹਨ(Path ਮਾਰਗ) throws IOException {
        return Files.readString(ਮਾਰਗ, StandardCharsets.UTF_8);
    }
    public static Path ਲਿਖਣ(Path ਮਾਰਗ, String ਤਤਕਰਾ_ਕੀਮਤ) throws IOException {
        return Files.writeString(ਮਾਰਗ, ਤਤਕਰਾ_ਕੀਮਤ, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path ਮਾਰਗ) throws IOException { return Files.readAllBytes(ਮਾਰਗ); }
    public static Path ਲਿੱਖੋ_ਬਾਈਟ_ਕੀਮਤ(Path ਮਾਰਗ, byte[] ਤਤਕਰਾ_ਕੀਮਤ) throws IOException { return Files.write(ਮਾਰਗ, ਤਤਕਰਾ_ਕੀਮਤ); }
    public static Path ਬਣਾਓ_ਨਿਰਦੇਸ਼ਕ(Path ਮਾਰਗ) throws IOException { return Files.createDirectories(ਮਾਰਗ); }
    public static boolean 있는가(Path ਮਾਰਗ) { return Files.exists(ਮਾਰਗ); }
    public static boolean 지우기(Path ਮਾਰਗ) throws IOException { return Files.deleteIfExists(ਮਾਰਗ); }
    public static List<Path> ਦਾਖਲਾ_ਸੂਚੀ(Path ਮਾਰਗ) throws IOException {
        try (Stream<Path> ਦਾਖਲਾ_ਕੀਮਤ = Files.list(ਮਾਰਗ)) { return ਦਾਖਲਾ_ਕੀਮਤ.sorted().collect(Collectors.toList()); }
    }
}
