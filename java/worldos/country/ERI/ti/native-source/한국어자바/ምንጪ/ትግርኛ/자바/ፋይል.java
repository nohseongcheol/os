// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ትግርኛ.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 ፋይል 도우미. */
public final class ፋይል {
    private ፋይል() {}
    public static Path መገዲ(String ሽም) { return Path.of(ሽም); }
    public static String 읽기(Path መገዲ) throws IOException {
        return Files.readString(መገዲ, StandardCharsets.UTF_8);
    }
    public static Path ጸሓፍ(Path መገዲ, String ትሕዝቶ_ዋጋ) throws IOException {
        return Files.writeString(መገዲ, ትሕዝቶ_ዋጋ, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path መገዲ) throws IOException { return Files.readAllBytes(መገዲ); }
    public static Path ጸሓፍ_ባይት_ዋጋ(Path መገዲ, byte[] ትሕዝቶ_ዋጋ) throws IOException { return Files.write(መገዲ, ትሕዝቶ_ዋጋ); }
    public static Path ፍጠር_ሓባሪ_ማህደር(Path መገዲ) throws IOException { return Files.createDirectories(መገዲ); }
    public static boolean 있는가(Path መገዲ) { return Files.exists(መገዲ); }
    public static boolean 지우기(Path መገዲ) throws IOException { return Files.deleteIfExists(መገዲ); }
    public static List<Path> ምእታው_ዝርዝር(Path መገዲ) throws IOException {
        try (Stream<Path> ምእታው_ዋጋ = Files.list(መገዲ)) { return ምእታው_ዋጋ.sorted().collect(Collectors.toList()); }
    }
}
