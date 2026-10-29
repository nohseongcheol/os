// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import polski.자바.*;
import java.nio.file.Path;
import java.awt.GraphicsEnvironment;
import javax.swing.*;

public class 인사 {
    public static void main(String[] argumenty) throws Exception {
        String tekst = "안녕하세요 · Hello · 日本語 · العربية · 😀";
        Path ścieżka_2 = nazwa_pliku.ścieżka_2("인사.txt");
        nazwa_pliku.Zapis(ścieżka_2, tekst);
        System.out.println(nazwa_pliku.Odczyt(ścieżka_2));
        Thread Praca_WARTOŚĆ = 작업.Uruchom_2("인사 작업", () -> System.out.println("작업 wątek_WARTOŚĆ Wykonaj_polecenie"));
        작업.기다리기(Praca_WARTOŚĆ);
        if (GraphicsEnvironment.isHeadless()) {
            System.out.println("그래픽 화면이 없어 interpretator_poleceń 출력만 실행했습니다. 창을 보려면 QEMU 데스크톱의 터미널에서 실행하세요.");
        } else {
            화면.나중에(() -> 화면.Okno("다국어 인사", new JLabel(tekst), 700, 160));
        }
    }
}
