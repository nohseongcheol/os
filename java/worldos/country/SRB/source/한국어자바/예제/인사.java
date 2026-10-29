// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자바.*;
import java.nio.file.Path;
import java.awt.GraphicsEnvironment;
import javax.swing.*;

public class 인사 {
    public static void main(String[] Аргументи) throws Exception {
        String Текст = "안녕하세요 · Hello · 日本語 · العربية · 😀";
        Path ПУТАЊА = Датотека.ПУТАЊА("인사.txt");
        Датотека.Пише(ПУТАЊА, Текст);
        System.out.println(Датотека.Чита(ПУТАЊА));
        Thread рад_вриједност = 작업.Покрени("인사 작업", () -> System.out.println("작업 нит_вриједност Изврши_команда"));
        작업.기다리기(рад_вриједност);
        if (GraphicsEnvironment.isHeadless()) {
            System.out.println("그래픽 화면이 없어 Терминал 출력만 실행했습니다. 창을 보려면 QEMU 데스크톱의 터미널에서 실행하세요.");
        } else {
            화면.나중에(() -> 화면.Прозор("다국어 인사", new JLabel(Текст), 700, 160));
        }
    }
}
