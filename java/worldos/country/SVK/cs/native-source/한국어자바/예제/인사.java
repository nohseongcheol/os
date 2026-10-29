// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import čeština.자바.*;
import java.nio.file.Path;
import java.awt.GraphicsEnvironment;
import javax.swing.*;

public class 인사 {
    public static void main(String[] argumenty) throws Exception {
        String text = "안녕하세요 · Hello · 日本語 · العربية · 😀";
        Path cesta_2 = název_souboru.cesta_2("인사.txt");
        název_souboru.Zápis(cesta_2, text);
        System.out.println(název_souboru.Čtení(cesta_2));
        Thread práce_HODNOTA = 작업.Spustit_2("인사 작업", () -> System.out.println("작업 vlákno_HODNOTA Provést_příkaz"));
        작업.기다리기(práce_HODNOTA);
        if (GraphicsEnvironment.isHeadless()) {
            System.out.println("그래픽 화면이 없어 interpret_příkazů 출력만 실행했습니다. 창을 보려면 QEMU 데스크톱의 터미널에서 실행하세요.");
        } else {
            화면.나중에(() -> 화면.Okno("다국어 인사", new JLabel(text), 700, 160));
        }
    }
}
