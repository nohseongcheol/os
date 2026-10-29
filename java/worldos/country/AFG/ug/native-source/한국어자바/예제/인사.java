// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자바.*;
import java.nio.file.Path;
import java.awt.GraphicsEnvironment;
import javax.swing.*;

public class 인사 {
    public static void main(String[] ئۆزگەرگۈچىلەر) throws Exception {
        String تېكىست = "안녕하세요 · Hello · 日本語 · العربية · 😀";
        Path يول = ھۆججەت.يول("인사.txt");
        ھۆججەت.ياز(يول, تېكىست);
        System.out.println(ھۆججەت.ئوقۇ(يول));
        Thread 일 = 작업.ئىجرا_قىل_2("인사 작업", () -> System.out.println("작업 ئېقىم_قىممىتى_5b72a632 ئىجرا_قىلىش_بۇيرۇق"));
        작업.기다리기(일);
        if (GraphicsEnvironment.isHeadless()) {
            System.out.println("그래픽 화면이 없어 تېرمىنال 출력만 실행했습니다. 창을 보려면 QEMU 데스크톱의 터미널에서 실행하세요.");
        } else {
            화면.나중에(() -> 화면.كۆزنەك("다국어 인사", new JLabel(تېكىست), 700, 160));
        }
    }
}
