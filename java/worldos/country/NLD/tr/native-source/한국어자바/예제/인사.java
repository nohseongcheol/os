// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Türkçe.자바.*;
import java.nio.file.Path;
import java.awt.GraphicsEnvironment;
import javax.swing.*;

public class 인사 {
    public static void main(String[] bağımsız_değişkenler) throws Exception {
        String metin = "안녕하세요 · Hello · 日本語 · العربية · 😀";
        Path yol = dosya.yol("인사.txt");
        dosya.Yazma(yol, metin);
        System.out.println(dosya.Okuma(yol));
        Thread iş_değer = 작업.çalıştır("인사 작업", () -> System.out.println("작업 yazışma_değer yürütmek_komut"));
        작업.기다리기(iş_değer);
        if (GraphicsEnvironment.isHeadless()) {
            System.out.println("그래픽 화면이 없어 uçbirim 출력만 실행했습니다. 창을 보려면 QEMU 데스크톱의 터미널에서 실행하세요.");
        } else {
            화면.나중에(() -> 화면.Pencere("다국어 인사", new JLabel(metin), 700, 160));
        }
    }
}
