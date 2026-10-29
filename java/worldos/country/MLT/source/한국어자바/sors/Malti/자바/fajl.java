// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Malti.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 fajl 도우미. */
public final class fajl {
    private fajl() {}
    public static Path mogħdija(String isem) { return Path.of(isem); }
    public static String 읽기(Path mogħdija) throws IOException {
        return Files.readString(mogħdija, StandardCharsets.UTF_8);
    }
    public static Path kiteb(Path mogħdija, String Kontenut_VALUE) throws IOException {
        return Files.writeString(mogħdija, Kontenut_VALUE, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path mogħdija) throws IOException { return Files.readAllBytes(mogħdija); }
    public static Path kiteb_byte_VALUE(Path mogħdija, byte[] Kontenut_VALUE) throws IOException { return Files.write(mogħdija, Kontenut_VALUE); }
    public static Path ħalaq_direttorju(Path mogħdija) throws IOException { return Files.createDirectories(mogħdija); }
    public static boolean 있는가(Path mogħdija) { return Files.exists(mogħdija); }
    public static boolean 지우기(Path mogħdija) throws IOException { return Files.deleteIfExists(mogħdija); }
    public static List<Path> entrata_Lista(Path mogħdija) throws IOException {
        try (Stream<Path> entrata_VALUE = Files.list(mogħdija)) { return entrata_VALUE.sorted().collect(Collectors.toList()); }
    }
}
