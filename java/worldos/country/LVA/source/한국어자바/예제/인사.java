// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Latviešu.자바.*;
import java.nio.file.Path;
import java.awt.GraphicsEnvironment;
import javax.swing.*;

public class 인사 {
    public static void main(String[] Parametri) throws Exception {
        String Teksts = "안녕하세요 · Hello · 日本語 · العربية · 😀";
        Path CEĻŠ = Fails.CEĻŠ("인사.txt");
        Fails.Rakstīt(CEĻŠ, Teksts);
        System.out.println(Fails.Lasīt(CEĻŠ));
        Thread Darba_VALUE = 작업.Palaist("인사 작업", () -> System.out.println("작업 saruna_VALUE Izpildīt_komanda"));
        작업.기다리기(Darba_VALUE);
        if (GraphicsEnvironment.isHeadless()) {
            System.out.println("그래픽 화면이 없어 Terminālis 출력만 실행했습니다. 창을 보려면 QEMU 데스크톱의 터미널에서 실행하세요.");
        } else {
            화면.나중에(() -> 화면.Logs("다국어 인사", new JLabel(Teksts), 700, 160));
        }
    }
}
