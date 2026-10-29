// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import हिंदी.자바.*;
import java.nio.file.Path;
import java.awt.GraphicsEnvironment;
import javax.swing.*;

public class अभिनन्दन_ae353e94 {
    public static void main(String[] तर्क) throws Exception {
        String पाठ = "안녕하세요 · Hello · 日本語 · العربية · 😀";
        Path पथ = संचिका.पथ("अभिनन्दन_ae353e94.txt");
        संचिका.लिखें(पथ, पाठ);
        System.out.println(संचिका.पढ़ें(पथ));
        Thread काम_मान = 작업.चलाएँ("अभिनन्दन_ae353e94 작업", () -> System.out.println("작업 थ्रेड_मान निष्पादित_करें_आदेश"));
        작업.기다리기(काम_मान);
        if (GraphicsEnvironment.isHeadless()) {
            System.out.println("그래픽 화면이 없어 आदेशपटल 출력만 실행했습니다. 창을 보려면 QEMU 데스크톱의 터미널에서 실행하세요.");
        } else {
            화면.나중에(() -> 화면.खिड़की("다국어 अभिनन्दन_ae353e94", new JLabel(पाठ), 700, 160));
        }
    }
}
