// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Íslenska.자바.*;
import java.nio.file.Path;
import java.awt.GraphicsEnvironment;
import javax.swing.*;

public class 인사 {
    public static void main(String[] Viðföng) throws Exception {
        String Texti = "안녕하세요 · Hello · 日本語 · العربية · 😀";
        Path SLÓÐ = Skrá.SLÓÐ("인사.txt");
        Skrá.Skrift(SLÓÐ, Texti);
        System.out.println(Skrá.Lestur(SLÓÐ));
        Thread vinna_VALUE = 작업.Keyra_2("인사 작업", () -> System.out.println("작업 þráður_VALUE keyra_skipun"));
        작업.기다리기(vinna_VALUE);
        if (GraphicsEnvironment.isHeadless()) {
            System.out.println("그래픽 화면이 없어 Skjáhermir 출력만 실행했습니다. 창을 보려면 QEMU 데스크톱의 터미널에서 실행하세요.");
        } else {
            화면.나중에(() -> 화면.Gluggi("다국어 인사", new JLabel(Texti), 700, 160));
        }
    }
}
