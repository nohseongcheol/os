// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import українська.자바.*;
import java.nio.file.Path;
import java.awt.GraphicsEnvironment;
import javax.swing.*;

public class 인사 {
    public static void main(String[] аргументи) throws Exception {
        String текст = "안녕하세요 · Hello · 日本語 · العربية · 😀";
        Path шлях = файл.шлях("인사.txt");
        файл.Запис(шлях, текст);
        System.out.println(файл.Читання(шлях));
        Thread робота_значення = 작업.запустити("인사 작업", () -> System.out.println("작업 потік_значення_5b72a632 Виконати_команда"));
        작업.기다리기(робота_значення);
        if (GraphicsEnvironment.isHeadless()) {
            System.out.println("그래픽 화면이 없어 термінал 출력만 실행했습니다. 창을 보려면 QEMU 데스크톱의 터미널에서 실행하세요.");
        } else {
            화면.나중에(() -> 화면.Вікно("다국어 인사", new JLabel(текст), 700, 160));
        }
    }
}
