// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자바.*;
import java.nio.file.Path;
import java.awt.GraphicsEnvironment;
import javax.swing.*;

public class 인사 {
    public static void main(String[] 인수) throws Exception {
        String ପାଠ୍ଯ = "안녕하세요 · Hello · 日本語 · العربية · 😀";
        Path ପଥ = ଫାଇଲ.ପଥ("인사.txt");
        ଫାଇଲ.ଲେଖନ୍ତୁ(ପଥ, ପାଠ୍ଯ);
        System.out.println(ଫାଇଲ.ପଢନ୍ତୁ(ପଥ));
        Thread 일 = 작업.ଚଳାନ୍ତୁ("인사 작업", () -> System.out.println("작업 ଧାରା_ମୂଲ୍ୟ ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ"));
        작업.기다리기(일);
        if (GraphicsEnvironment.isHeadless()) {
            System.out.println("그래픽 화면이 없어 ଟର୍ମିନାଲ 출력만 실행했습니다. 창을 보려면 QEMU 데스크톱의 터미널에서 실행하세요.");
        } else {
            화면.나중에(() -> 화면.ଓ୍ୱିଣ୍ଡୋ("다국어 인사", new JLabel(ପାଠ୍ଯ), 700, 160));
        }
    }
}
