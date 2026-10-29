// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Română.자바.*;
import java.nio.file.Path;
import java.awt.GraphicsEnvironment;
import javax.swing.*;

public class 인사 {
    public static void main(String[] Argumente) throws Exception {
        String SMS = "안녕하세요 · Hello · 日本語 · العربية · 😀";
        Path Cale = Fișier.Cale("인사.txt");
        Fișier.Scriere(Cale, SMS);
        System.out.println(Fișier.Citire(Cale));
        Thread Birou_VALUE = 작업.Pornește("인사 작업", () -> System.out.println("작업 fir_VALUE executa_comandă"));
        작업.기다리기(Birou_VALUE);
        if (GraphicsEnvironment.isHeadless()) {
            System.out.println("그래픽 화면이 없어 Terminal 출력만 실행했습니다. 창을 보려면 QEMU 데스크톱의 터미널에서 실행하세요.");
        } else {
            화면.나중에(() -> 화면.Fereastră("다국어 인사", new JLabel(SMS), 700, 160));
        }
    }
}
