// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자바.*;
import java.nio.file.Path;
import java.awt.GraphicsEnvironment;
import javax.swing.*;

public class 인사 {
    public static void main(String[] Аргументтер) throws Exception {
        String Мәтін = "안녕하세요 · Hello · 日本語 · العربية · 😀";
        Path Жол_2 = Файл.Жол_2("인사.txt");
        Файл.Жазу(Жол_2, Мәтін);
        System.out.println(Файл.Оқу(Жол_2));
        Thread жұмыс_мән = 작업.Орындау_2("인사 작업", () -> System.out.println("작업 ағын_мән орындау_пәрмен"));
        작업.기다리기(жұмыс_мән);
        if (GraphicsEnvironment.isHeadless()) {
            System.out.println("그래픽 화면이 없어 Терминал 출력만 실행했습니다. 창을 보려면 QEMU 데스크톱의 터미널에서 실행하세요.");
        } else {
            화면.나중에(() -> 화면.Терезе("다국어 인사", new JLabel(Мәтін), 700, 160));
        }
    }
}
