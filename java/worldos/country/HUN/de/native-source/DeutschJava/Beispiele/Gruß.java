// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Deutsch.Java.*;
import java.nio.file.Path;
import java.awt.GraphicsEnvironment;
import javax.swing.*;

public class Gruß {
    public static void main(String[] argumente) throws Exception {
        String Text = "안녕하세요 · Hello · 日本語 · العربية · 😀";
        Path pfad = Datei.pfad("Gruß.txt");
        Datei.schreiben(pfad, Text);
        System.out.println(Datei.lesen(pfad));
        Thread arbeitWert = Aufgabe.ausführenVorgang("Gruß Aufgabe", () -> System.out.println("Aufgabe ausführungsfadenWert befehlAusführen"));
        Aufgabe.abwarten(arbeitWert);
        if (GraphicsEnvironment.isHeadless()) {
            System.out.println("그래픽 화면이 없어 terminal 출력만 실행했습니다. 창을 보려면 QEMU 데스크톱의 터미널에서 실행하세요.");
        } else {
            Bildschirm.späterWert(() -> Bildschirm.fenster("다국어 Gruß", new JLabel(Text), 700, 160));
        }
    }
}
