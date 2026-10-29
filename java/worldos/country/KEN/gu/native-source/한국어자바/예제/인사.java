// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import ગુજરાતી.자바.*;
import java.nio.file.Path;
import java.awt.GraphicsEnvironment;
import javax.swing.*;

public class 인사 {
    public static void main(String[] દલીલો) throws Exception {
        String લખાણ = "안녕하세요 · Hello · 日本語 · العربية · 😀";
        Path પથ = ફાઈલ.પથ("인사.txt");
        ફાઈલ.લખો(પથ, લખાણ);
        System.out.println(ફાઈલ.વાંચો(પથ));
        Thread કાર્યસ્થાન_મૂલ્ય = 작업.ચલાવો_2("인사 작업", () -> System.out.println("작업 થ્રેડ_મૂલ્ય અમલ_કરો_આદેશ"));
        작업.기다리기(કાર્યસ્થાન_મૂલ્ય);
        if (GraphicsEnvironment.isHeadless()) {
            System.out.println("그래픽 화면이 없어 ટર્મિનલ 출력만 실행했습니다. 창을 보려면 QEMU 데스크톱의 터미널에서 실행하세요.");
        } else {
            화면.나중에(() -> 화면.વિંડો("다국어 인사", new JLabel(લખાણ), 700, 160));
        }
    }
}
