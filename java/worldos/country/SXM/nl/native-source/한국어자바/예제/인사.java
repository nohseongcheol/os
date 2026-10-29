// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Nederlands.자바.*;
import java.nio.file.Path;
import java.awt.GraphicsEnvironment;
import javax.swing.*;

public class 인사 {
    public static void main(String[] argumenten) throws Exception {
        String tekst = "안녕하세요 · Hello · 日本語 · العربية · 😀";
        Path pad = bestand.pad("인사.txt");
        bestand.Schrijven(pad, tekst);
        System.out.println(bestand.Lezen(pad));
        Thread Werk_WAARDE = 작업.starten("인사 작업", () -> System.out.println("작업 thread_WAARDE Uitvoeren_opdracht"));
        작업.기다리기(Werk_WAARDE);
        if (GraphicsEnvironment.isHeadless()) {
            System.out.println("그래픽 화면이 없어 terminal 출력만 실행했습니다. 창을 보려면 QEMU 데스크톱의 터미널에서 실행하세요.");
        } else {
            scherm.나중에(() -> scherm.Venster("다국어 인사", new JLabel(tekst), 700, 160));
        }
    }
}
