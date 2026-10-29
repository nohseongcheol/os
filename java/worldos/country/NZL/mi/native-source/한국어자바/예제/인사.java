// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Reo_Māori.자바.*;
import java.nio.file.Path;
import java.awt.GraphicsEnvironment;
import javax.swing.*;

public class 인사 {
    public static void main(String[] 인수) throws Exception {
        String Ngā_kupu = "안녕하세요 · Hello · 日本語 · العربية · 😀";
        Path ara = Kōnae.ara("인사.txt");
        Kōnae.Tuhia(ara, Ngā_kupu);
        System.out.println(Kōnae.Pānuitia(ara));
        Thread 일 = 작업.whakahaere("인사 작업", () -> System.out.println("작업 miro_uara kawe_tono"));
        작업.기다리기(일);
        if (GraphicsEnvironment.isHeadless()) {
            System.out.println("그래픽 화면이 없어 Tauranga 출력만 실행했습니다. 창을 보려면 QEMU 데스크톱의 터미널에서 실행하세요.");
        } else {
            화면.나중에(() -> 화면.matapihi("다국어 인사", new JLabel(Ngā_kupu), 700, 160));
        }
    }
}
