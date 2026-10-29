// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Български.자바.*;
import java.nio.file.Path;
import java.awt.GraphicsEnvironment;
import javax.swing.*;

public class 인사 {
    public static void main(String[] Параметри) throws Exception {
        String Текст = "안녕하세요 · Hello · 日本語 · العربية · 😀";
        Path ПЪТ = Файл.ПЪТ("인사.txt");
        Файл.Писане(ПЪТ, Текст);
        System.out.println(Файл.Четене(ПЪТ));
        Thread работа_стойност = 작업.Стартиране("인사 작업", () -> System.out.println("작업 нишка_стойност изпълнявам_команда"));
        작업.기다리기(работа_стойност);
        if (GraphicsEnvironment.isHeadless()) {
            System.out.println("그래픽 화면이 없어 Терминал 출력만 실행했습니다. 창을 보려면 QEMU 데스크톱의 터미널에서 실행하세요.");
        } else {
            화면.나중에(() -> 화면.Прозорец("다국어 인사", new JLabel(Текст), 700, 160));
        }
    }
}
