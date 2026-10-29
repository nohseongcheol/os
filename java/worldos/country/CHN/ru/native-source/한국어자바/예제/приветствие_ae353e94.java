// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import русский.자바.*;
import java.nio.file.Path;
import java.awt.GraphicsEnvironment;
import javax.swing.*;

public class приветствие_ae353e94 {
    public static void main(String[] аргументы) throws Exception {
        String текст = "안녕하세요 · Hello · 日本語 · العربية · 😀";
        Path путь = файл.путь("приветствие_ae353e94.txt");
        файл.Запись(путь, текст);
        System.out.println(файл.Чтение(путь));
        Thread работа_ЗНАЧЕН = 작업.запустить("приветствие_ae353e94 작업", () -> System.out.println("작업 поток_ЗНАЧЕН_5b72a632 실행"));
        작업.기다리기(работа_ЗНАЧЕН);
        if (GraphicsEnvironment.isHeadless()) {
            System.out.println("그래픽 화면이 없어 терминал 출력만 실행했습니다. 창을 보려면 QEMU 데스크톱의 터미널에서 실행하세요.");
        } else {
            экран.나중에(() -> экран.Окно("다국어 приветствие_ae353e94", new JLabel(текст), 700, 160));
        }
    }
}
