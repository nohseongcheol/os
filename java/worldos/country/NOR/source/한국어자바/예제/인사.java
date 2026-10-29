// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import norsk.자바.*;
import java.nio.file.Path;
import java.awt.GraphicsEnvironment;
import javax.swing.*;

public class 인사 {
    public static void main(String[] Argumenter) throws Exception {
        String Tekst = "안녕하세요 · Hello · 日本語 · العربية · 😀";
        Path Sti = Fil.Sti("인사.txt");
        Fil.Skriv(Sti, Tekst);
        System.out.println(Fil.Les(Sti));
        Thread Arbeid_VERDI = 작업.Kjør_2("인사 작업", () -> System.out.println("작업 tråd_VERDI Utfør_kommando"));
        작업.기다리기(Arbeid_VERDI);
        if (GraphicsEnvironment.isHeadless()) {
            System.out.println("그래픽 화면이 없어 Terminal 출력만 실행했습니다. 창을 보려면 QEMU 데스크톱의 터미널에서 실행하세요.");
        } else {
            skjermbilde.나중에(() -> skjermbilde.Vindu("다국어 인사", new JLabel(Tekst), 700, 160));
        }
    }
}
