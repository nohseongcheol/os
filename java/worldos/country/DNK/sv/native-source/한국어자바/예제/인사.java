// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Svenska.자바.*;
import java.nio.file.Path;
import java.awt.GraphicsEnvironment;
import javax.swing.*;

public class 인사 {
    public static void main(String[] argument) throws Exception {
        String text = "안녕하세요 · Hello · 日本語 · العربية · 😀";
        Path sökväg_2 = filnamn.sökväg_2("인사.txt");
        filnamn.Skriv(sökväg_2, text);
        System.out.println(filnamn.Läs(sökväg_2));
        Thread Arbete_värde = 작업.Kör("인사 작업", () -> System.out.println("작업 tråd_värde köra_kommando"));
        작업.기다리기(Arbete_värde);
        if (GraphicsEnvironment.isHeadless()) {
            System.out.println("그래픽 화면이 없어 kommandotolk 출력만 실행했습니다. 창을 보려면 QEMU 데스크톱의 터미널에서 실행하세요.");
        } else {
            skärmbild.나중에(() -> skärmbild.Fönster("다국어 인사", new JLabel(text), 700, 160));
        }
    }
}
