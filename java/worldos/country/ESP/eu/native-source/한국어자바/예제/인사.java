// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Euskara.자바.*;
import java.nio.file.Path;
import java.awt.GraphicsEnvironment;
import javax.swing.*;

public class 인사 {
    public static void main(String[] Argumentuak) throws Exception {
        String Testua = "안녕하세요 · Hello · 日本語 · العربية · 😀";
        Path Bide_izena = Fitxategia.Bide_izena("인사.txt");
        Fitxategia.Idatzi(Bide_izena, Testua);
        System.out.println(Fitxategia.Irakurri(Bide_izena));
        Thread lan_balio = 작업.Exekutatu_2("인사 작업", () -> System.out.println("작업 hari_balio exekutatu_komando"));
        작업.기다리기(lan_balio);
        if (GraphicsEnvironment.isHeadless()) {
            System.out.println("그래픽 화면이 없어 Terminala 출력만 실행했습니다. 창을 보려면 QEMU 데스크톱의 터미널에서 실행하세요.");
        } else {
            화면.나중에(() -> 화면.Leihoa("다국어 인사", new JLabel(Testua), 700, 160));
        }
    }
}
