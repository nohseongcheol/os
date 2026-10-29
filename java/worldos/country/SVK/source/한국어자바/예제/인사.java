// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Slovenský.자바.*;
import java.nio.file.Path;
import java.awt.GraphicsEnvironment;
import javax.swing.*;

public class 인사 {
    public static void main(String[] Argumenty) throws Exception {
        String Spracovanie_textu = "안녕하세요 · Hello · 日本語 · العربية · 😀";
        Path Cesta = Súbor.Cesta("인사.txt");
        Súbor.Zápis(Cesta, Spracovanie_textu);
        System.out.println(Súbor.Čítanie(Cesta));
        Thread Práca_VALUE = 작업.Spustiť_2("인사 작업", () -> System.out.println("작업 vlákno_VALUE Vykonať_príkaz"));
        작업.기다리기(Práca_VALUE);
        if (GraphicsEnvironment.isHeadless()) {
            System.out.println("그래픽 화면이 없어 Terminál 출력만 실행했습니다. 창을 보려면 QEMU 데스크톱의 터미널에서 실행하세요.");
        } else {
            화면.나중에(() -> 화면.Okno("다국어 인사", new JLabel(Spracovanie_textu), 700, 160));
        }
    }
}
