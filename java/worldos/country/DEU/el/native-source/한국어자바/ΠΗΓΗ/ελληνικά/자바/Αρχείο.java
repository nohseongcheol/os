// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ελληνικά.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 Αρχείο βοηθητική_εφαρμογή_τιμή. */
public final class Αρχείο {
    private Αρχείο() {}
    public static Path ΔΙΑΔΡΟΜΗ(String Όνομα) { return Path.of(Όνομα); }
    public static String Ανάγνωση(Path ΔΙΑΔΡΟΜΗ) throws IOException {
        return Files.readString(ΔΙΑΔΡΟΜΗ, StandardCharsets.UTF_8);
    }
    public static Path Εγγραφή(Path ΔΙΑΔΡΟΜΗ, String Περιεχόμενο_τιμή) throws IOException {
        return Files.writeString(ΔΙΑΔΡΟΜΗ, Περιεχόμενο_τιμή, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path ΔΙΑΔΡΟΜΗ) throws IOException { return Files.readAllBytes(ΔΙΑΔΡΟΜΗ); }
    public static Path 바이트쓰기(Path ΔΙΑΔΡΟΜΗ, byte[] Περιεχόμενο_τιμή) throws IOException { return Files.write(ΔΙΑΔΡΟΜΗ, Περιεχόμενο_τιμή); }
    public static Path ανοίγω_Κατάλογος(Path ΔΙΑΔΡΟΜΗ) throws IOException { return Files.createDirectories(ΔΙΑΔΡΟΜΗ); }
    public static boolean 있는가(Path ΔΙΑΔΡΟΜΗ) { return Files.exists(ΔΙΑΔΡΟΜΗ); }
    public static boolean διαγράφω_καταχώρηση(Path ΔΙΑΔΡΟΜΗ) throws IOException { return Files.deleteIfExists(ΔΙΑΔΡΟΜΗ); }
    public static List<Path> καταχώρηση_Λίστα(Path ΔΙΑΔΡΟΜΗ) throws IOException {
        try (Stream<Path> καταχώρηση_τιμή = Files.list(ΔΙΑΔΡΟΜΗ)) { return καταχώρηση_τιμή.sorted().collect(Collectors.toList()); }
    }
}
