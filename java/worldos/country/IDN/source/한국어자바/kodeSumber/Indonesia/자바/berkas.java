// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Indonesia.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 berkas 도우미. */
public final class berkas {
    private berkas() {}
    public static Path jalur(String Nama_2) { return Path.of(Nama_2); }
    public static String Baca(Path jalur) throws IOException {
        return Files.readString(jalur, StandardCharsets.UTF_8);
    }
    public static Path Tulis(Path jalur, String Isi_VALUE) throws IOException {
        return Files.writeString(jalur, Isi_VALUE, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path jalur) throws IOException { return Files.readAllBytes(jalur); }
    public static Path tulis_byte_VALUE(Path jalur, byte[] Isi_VALUE) throws IOException { return Files.write(jalur, Isi_VALUE); }
    public static Path Buat_Direktori(Path jalur) throws IOException { return Files.createDirectories(jalur); }
    public static boolean 있는가(Path jalur) { return Files.exists(jalur); }
    public static boolean hapus_entri_c8dbc399(Path jalur) throws IOException { return Files.deleteIfExists(jalur); }
    public static List<Path> entri_Daftar(Path jalur) throws IOException {
        try (Stream<Path> entri_VALUE = Files.list(jalur)) { return entri_VALUE.sorted().collect(Collectors.toList()); }
    }
}
