// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** 표준 Path와 IOException을 그대로 사용하는 UTF-8 फायल 도우미. */
public final class फायल {
    private फायल() {}
    public static Path पाथ(String नांव) { return Path.of(नांव); }
    public static String 읽기(Path पाथ) throws IOException {
        return Files.readString(पाथ, StandardCharsets.UTF_8);
    }
    public static Path बरोवचें(Path पाथ, String अनुक्रमणिका_मोल) throws IOException {
        return Files.writeString(पाथ, अनुक्रमणिका_मोल, StandardCharsets.UTF_8);
    }
    public static byte[] 바이트읽기(Path पाथ) throws IOException { return Files.readAllBytes(पाथ); }
    public static Path बरोवचें_बायट_मोल(Path पाथ, byte[] अनुक्रमणिका_मोल) throws IOException { return Files.write(पाथ, अनुक्रमणिका_मोल); }
    public static Path निर्माण_करचें_नामावळ(Path पाथ) throws IOException { return Files.createDirectories(पाथ); }
    public static boolean 있는가(Path पाथ) { return Files.exists(पाथ); }
    public static boolean 지우기(Path पाथ) throws IOException { return Files.deleteIfExists(पाथ); }
    public static List<Path> प्रवेश_सुची(Path पाथ) throws IOException {
        try (Stream<Path> प्रवेश_मोल = Files.list(पाथ)) { return प्रवेश_मोल.sorted().collect(Collectors.toList()); }
    }
}
