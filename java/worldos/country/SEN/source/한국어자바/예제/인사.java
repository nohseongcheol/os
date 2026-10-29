// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자바.*;
import java.nio.file.Path;
import java.awt.GraphicsEnvironment;
import javax.swing.*;

public class 인사 {
    public static void main(String[] 인수) throws Exception {
        String Tekst = "안녕하세요 · Hello · 日本語 · العربية · 😀";
        Path Yoonu_jëmale = bara_denc.Yoonu_jëmale("인사.txt");
        bara_denc.biir(Yoonu_jëmale, Tekst);
        System.out.println(bara_denc.읽기(Yoonu_jëmale));
        Thread 일 = 작업.daw("인사 작업", () -> System.out.println("작업 buumug_jokkale_xëyma def_ndigel"));
        작업.기다리기(일);
        if (GraphicsEnvironment.isHeadless()) {
            System.out.println("그래픽 화면이 없어 터미널 출력만 실행했습니다. 창을 보려면 QEMU 데스크톱의 터미널에서 실행하세요.");
        } else {
            화면.나중에(() -> 화면.palanteer("다국어 인사", new JLabel(Tekst), 700, 160));
        }
    }
}
