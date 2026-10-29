// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import עברית.자바.*;
import java.nio.file.Path;
import java.awt.GraphicsEnvironment;
import javax.swing.*;

public class 인사 {
    public static void main(String[] ארגומנטים) throws Exception {
        String טקסט = "안녕하세요 · Hello · 日本語 · العربية · 😀";
        Path נתיב = קובץ.נתיב("인사.txt");
        קובץ.כתוב(נתיב, טקסט);
        System.out.println(קובץ.קרא(נתיב));
        Thread עבודה_ערך = 작업.הפעלה("인사 작업", () -> System.out.println("작업 שרשור_ערך לבצע_פקודה"));
        작업.기다리기(עבודה_ערך);
        if (GraphicsEnvironment.isHeadless()) {
            System.out.println("그래픽 화면이 없어 מסוף 출력만 실행했습니다. 창을 보려면 QEMU 데스크톱의 터미널에서 실행하세요.");
        } else {
            화면.나중에(() -> 화면.חלון("다국어 인사", new JLabel(טקסט), 700, 160));
        }
    }
}
