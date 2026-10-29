// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 Fayil 도우미. */
public final class Fayil {
    private Fayil() {}
    public static Path Hanyar_shiga(String Suna) { return Path.of(Suna); }
    public static String Yi_Karatu(Path Hanyar_shiga) throws IOException {
        return Files.readString(Hanyar_shiga, StandardCharsets.UTF_8);
    }
    public static Path Yi_Rubutu(Path Hanyar_shiga, String kunshiya_Daraja) throws IOException {
        return Files.writeString(Hanyar_shiga, kunshiya_Daraja, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path Hanyar_shiga) throws IOException { return Files.readAllBytes(Hanyar_shiga); }
    public static Path Rubuta_bayit_Daraja(Path Hanyar_shiga, byte[] kunshiya_Daraja) throws IOException { return Files.write(Hanyar_shiga, kunshiya_Daraja); }
    public static Path ƙirƙíra_ma_ajiya(Path Hanyar_shiga) throws IOException { return Files.createDirectories(Hanyar_shiga); }
    public static boolean 있는가(Path Hanyar_shiga) { return Files.exists(Hanyar_shiga); }
    public static boolean share_Mashigar_bayanai(Path Hanyar_shiga) throws IOException { return Files.deleteIfExists(Hanyar_shiga); }
    public static List<Path> Mashigar_bayanai_Jeri(Path Hanyar_shiga) throws IOException {
        try (Stream<Path> Mashigar_bayanai_Daraja = Files.list(Hanyar_shiga)) { return Mashigar_bayanai_Daraja.sorted().collect(Collectors.toList()); }
    }
}
