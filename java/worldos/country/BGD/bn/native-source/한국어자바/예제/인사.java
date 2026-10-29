// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import বাংলা.자바.*;
import java.nio.file.Path;
import java.awt.GraphicsEnvironment;
import javax.swing.*;

public class 인사 {
    public static void main(String[] আর্গুমেন্ট_তালিকা) throws Exception {
        String পাঠ = "안녕하세요 · Hello · 日本語 · العربية · 😀";
        Path পথ_2 = নথির_নাম.পথ_2("인사.txt");
        নথির_নাম.লেখা(পথ_2, পাঠ);
        System.out.println(নথির_নাম.পড়া(পথ_2));
        Thread কর্মক্ষেত্র_মান = 작업.চালনা("인사 작업", () -> System.out.println("작업 থ্রেড_মান কার্যকর_করুন_আদেশ"));
        작업.기다리기(কর্মক্ষেত্র_মান);
        if (GraphicsEnvironment.isHeadless()) {
            System.out.println("그래픽 화면이 없어 আদেশ_ব্যাখ্যাকারী 출력만 실행했습니다. 창을 보려면 QEMU 데스크톱의 터미널에서 실행하세요.");
        } else {
            화면.나중에(() -> 화면.উইন্ডো("다국어 인사", new JLabel(পাঠ), 700, 160));
        }
    }
}
