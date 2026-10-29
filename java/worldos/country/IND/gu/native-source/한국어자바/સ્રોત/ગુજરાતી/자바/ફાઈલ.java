// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ગુજરાતી.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 ફાઈલ 도우미. */
public final class ફાઈલ {
    private ફાઈલ() {}
    public static Path પથ(String નામ) { return Path.of(નામ); }
    public static String વાંચો(Path પથ) throws IOException {
        return Files.readString(પથ, StandardCharsets.UTF_8);
    }
    public static Path લખો(Path પથ, String સામગ્રી_મૂલ્ય) throws IOException {
        return Files.writeString(પથ, સામગ્રી_મૂલ્ય, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path પથ) throws IOException { return Files.readAllBytes(પથ); }
    public static Path લખો_બાઇટ_મૂલ્ય(Path પથ, byte[] સામગ્રી_મૂલ્ય) throws IOException { return Files.write(પથ, સામગ્રી_મૂલ્ય); }
    public static Path બનાવો_નિર્દેશિકા(Path પથ) throws IOException { return Files.createDirectories(પથ); }
    public static boolean 있는가(Path પથ) { return Files.exists(પથ); }
    public static boolean 지우기(Path પથ) throws IOException { return Files.deleteIfExists(પથ); }
    public static List<Path> પ્રવેશ_સૂચી(Path પથ) throws IOException {
        try (Stream<Path> પ્રવેશ_મૂલ્ય = Files.list(પથ)) { return પ્રવેશ_મૂલ્ય.sorted().collect(Collectors.toList()); }
    }
}
