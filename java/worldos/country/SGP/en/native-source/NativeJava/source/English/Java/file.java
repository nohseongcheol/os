// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package English.Java;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** UTF-8 file helper using standard Path and IOException directly. */
public final class file {
    private file() {}
    public static Path path(String name) { return Path.of(name); }
    public static String read(Path path) throws IOException {
        return Files.readString(path, StandardCharsets.UTF_8);
    }
    public static Path write(Path path, String contentValue) throws IOException {
        return Files.writeString(path, contentValue, StandardCharsets.UTF_8);
    }
    public static byte[] readByteValue(Path path) throws IOException { return Files.readAllBytes(path); }
    public static Path writeByteValue(Path path, byte[] contentValue) throws IOException { return Files.write(path, contentValue); }
    public static Path createDirectory(Path path) throws IOException { return Files.createDirectories(path); }
    public static boolean doesExist(Path path) { return Files.exists(path); }
    public static boolean eraseEntry(Path path) throws IOException { return Files.deleteIfExists(path); }
    public static List<Path> entryList(Path path) throws IOException {
        try (Stream<Path> entryValue = Files.list(path)) { return entryValue.sorted().collect(Collectors.toList()); }
    }
}
