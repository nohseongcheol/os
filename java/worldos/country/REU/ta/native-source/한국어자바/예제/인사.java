// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import தமிழ்.자바.*;
import java.nio.file.Path;
import java.awt.GraphicsEnvironment;
import javax.swing.*;

public class 인사 {
    public static void main(String[] செயலுருபுகள்) throws Exception {
        String உரை = "안녕하세요 · Hello · 日本語 · العربية · 😀";
        Path பாதை_2 = கோப்பின்_பெயர்.பாதை_2("인사.txt");
        கோப்பின்_பெயர்.எழுது(பாதை_2, உரை);
        System.out.println(கோப்பின்_பெயர்.படி(பாதை_2));
        Thread பணி_மதிப்பு = 작업.செயல்படுத்துக("인사 작업", () -> System.out.println("작업 தொடரிழை_மதிப்பு இயக்கு_கட்டளை"));
        작업.기다리기(பணி_மதிப்பு);
        if (GraphicsEnvironment.isHeadless()) {
            System.out.println("그래픽 화면이 없어 கட்டளை_விளக்கி 출력만 실행했습니다. 창을 보려면 QEMU 데스크톱의 터미널에서 실행하세요.");
        } else {
            화면.나중에(() -> 화면.சாளரம்("다국어 인사", new JLabel(உரை), 700, 160));
        }
    }
}
