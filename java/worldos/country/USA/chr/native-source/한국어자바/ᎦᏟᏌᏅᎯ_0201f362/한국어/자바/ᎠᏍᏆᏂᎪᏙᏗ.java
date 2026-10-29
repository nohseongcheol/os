// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 ᎠᏍᏆᏂᎪᏙᏗ 도우미. */
public final class ᎠᏍᏆᏂᎪᏙᏗ {
    private ᎠᏍᏆᏂᎪᏙᏗ() {}
    public static Path ᎠᏍᏓᏩᏛᏍᏗ(String ᏚᏙᎥᎢ) { return Path.of(ᏚᏙᎥᎢ); }
    public static String 읽기(Path ᎠᏍᏓᏩᏛᏍᏗ) throws IOException {
        return Files.readString(ᎠᏍᏓᏩᏛᏍᏗ, StandardCharsets.UTF_8);
    }
    public static Path ᎪᏪᎶᏗ(Path ᎠᏍᏓᏩᏛᏍᏗ, String ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ) throws IOException {
        return Files.writeString(ᎠᏍᏓᏩᏛᏍᏗ, ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path ᎠᏍᏓᏩᏛᏍᏗ) throws IOException { return Files.readAllBytes(ᎠᏍᏓᏩᏛᏍᏗ); }
    public static Path ᎪᏪᎶᏗ_byte_ᏧᎬᏩᎶᏗᏯ(Path ᎠᏍᏓᏩᏛᏍᏗ, byte[] ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ) throws IOException { return Files.write(ᎠᏍᏓᏩᏛᏍᏗ, ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ); }
    public static Path 폴더만들기(Path ᎠᏍᏓᏩᏛᏍᏗ) throws IOException { return Files.createDirectories(ᎠᏍᏓᏩᏛᏍᏗ); }
    public static boolean 있는가(Path ᎠᏍᏓᏩᏛᏍᏗ) { return Files.exists(ᎠᏍᏓᏩᏛᏍᏗ); }
    public static boolean 지우기(Path ᎠᏍᏓᏩᏛᏍᏗ) throws IOException { return Files.deleteIfExists(ᎠᏍᏓᏩᏛᏍᏗ); }
    public static List<Path> Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏕᎦᏅᏅᏛ(Path ᎠᏍᏓᏩᏛᏍᏗ) throws IOException {
        try (Stream<Path> Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ = Files.list(ᎠᏍᏓᏩᏛᏍᏗ)) { return Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.sorted().collect(Collectors.toList()); }
    }
}
