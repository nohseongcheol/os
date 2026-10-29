// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자바.*;
import java.nio.file.Path;
import java.awt.GraphicsEnvironment;
import javax.swing.*;

public class 인사 {
    public static void main(String[] 인수) throws Exception {
        String പദാവലി = "안녕하세요 · Hello · 日本語 · العربية · 😀";
        Path വഴി = ഫയല്.വഴി("인사.txt");
        ഫയല്.എഴുത്തു്(വഴി, പദാവലി);
        System.out.println(ഫയല്.വായന(വഴി));
        Thread തൊഴിലിടം_മൂല്യം = 작업.നടപ്പിലാക്കുക("인사 작업", () -> System.out.println("작업 ത്രെഡ്_മൂല്യം നടപ്പാക്കുക_കമാന്_ഡ്"));
        작업.기다리기(തൊഴിലിടം_മൂല്യം);
        if (GraphicsEnvironment.isHeadless()) {
            System.out.println("그래픽 화면이 없어 ടെ_ര്മിനല് 출력만 실행했습니다. 창을 보려면 QEMU 데스크톱의 터미널에서 실행하세요.");
        } else {
            화면.나중에(() -> 화면.ജാലകം("다국어 인사", new JLabel(പദാവലി), 700, 160));
        }
    }
}
