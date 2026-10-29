// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 ຟາຍ 도우미. */
public final class ຟາຍ {
    private ຟາຍ() {}
    public static Path ທາງໂຄຈອນ(String ຊື່) { return Path.of(ຊື່); }
    public static String 읽기(Path ທາງໂຄຈອນ) throws IOException {
        return Files.readString(ທາງໂຄຈອນ, StandardCharsets.UTF_8);
    }
    public static Path ຂຽນ(Path ທາງໂຄຈອນ, String ເນື້ອໃນ_ຄ່າ_cb0f2404) throws IOException {
        return Files.writeString(ທາງໂຄຈອນ, ເນື້ອໃນ_ຄ່າ_cb0f2404, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path ທາງໂຄຈອນ) throws IOException { return Files.readAllBytes(ທາງໂຄຈອນ); }
    public static Path ຂຽນ_ໄບ_ຄ່າ(Path ທາງໂຄຈອນ, byte[] ເນື້ອໃນ_ຄ່າ_cb0f2404) throws IOException { return Files.write(ທາງໂຄຈອນ, ເນື້ອໃນ_ຄ່າ_cb0f2404); }
    public static Path ສ້າງ_ກຸ່ມຂໍ້ມູນ(Path ທາງໂຄຈອນ) throws IOException { return Files.createDirectories(ທາງໂຄຈອນ); }
    public static boolean 있는가(Path ທາງໂຄຈອນ) { return Files.exists(ທາງໂຄຈອນ); }
    public static boolean ລຶບ_ເຂົ້າໃນ(Path ທາງໂຄຈອນ) throws IOException { return Files.deleteIfExists(ທາງໂຄຈອນ); }
    public static List<Path> ເຂົ້າໃນ_ລາຍຊື່(Path ທາງໂຄຈອນ) throws IOException {
        try (Stream<Path> ເຂົ້າໃນ_ຄ່າ = Files.list(ທາງໂຄຈອນ)) { return ເຂົ້າໃນ_ຄ່າ.sorted().collect(Collectors.toList()); }
    }
}
