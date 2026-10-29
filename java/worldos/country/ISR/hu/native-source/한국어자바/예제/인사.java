// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import magyar.자바.*;
import java.nio.file.Path;
import java.awt.GraphicsEnvironment;
import javax.swing.*;

public class 인사 {
    public static void main(String[] Argumentumok) throws Exception {
        String Szöveg = "안녕하세요 · Hello · 日本語 · العربية · 😀";
        Path ÚTVONAL = Fájl.ÚTVONAL("인사.txt");
        Fájl.Írás(ÚTVONAL, Szöveg);
        System.out.println(Fájl.Olvasás(ÚTVONAL));
        Thread munka_ÉRTÉK = 작업.Futtatás("인사 작업", () -> System.out.println("작업 szál_ÉRTÉK végrehajt_parancs"));
        작업.기다리기(munka_ÉRTÉK);
        if (GraphicsEnvironment.isHeadless()) {
            System.out.println("그래픽 화면이 없어 Terminál 출력만 실행했습니다. 창을 보려면 QEMU 데스크톱의 터미널에서 실행하세요.");
        } else {
            화면.나중에(() -> 화면.Ablak("다국어 인사", new JLabel(Szöveg), 700, 160));
        }
    }
}
