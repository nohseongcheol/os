// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import ελληνικά.자바.*;
import java.nio.file.Path;
import java.awt.GraphicsEnvironment;
import javax.swing.*;

public class 인사 {
    public static void main(String[] Παράμετροι) throws Exception {
        String Κείμενο = "안녕하세요 · Hello · 日本語 · العربية · 😀";
        Path ΔΙΑΔΡΟΜΗ = Αρχείο.ΔΙΑΔΡΟΜΗ("인사.txt");
        Αρχείο.Εγγραφή(ΔΙΑΔΡΟΜΗ, Κείμενο);
        System.out.println(Αρχείο.Ανάγνωση(ΔΙΑΔΡΟΜΗ));
        Thread Εργασία_τιμή = 작업.Εκτέλεση_2("인사 작업", () -> System.out.println("작업 νήμα_τιμή εκτελώ_εντολή"));
        작업.기다리기(Εργασία_τιμή);
        if (GraphicsEnvironment.isHeadless()) {
            System.out.println("그래픽 화면이 없어 Τερματικό 출력만 실행했습니다. 창을 보려면 QEMU 데스크톱의 터미널에서 실행하세요.");
        } else {
            화면.나중에(() -> 화면.Παράθυρο("다국어 인사", new JLabel(Κείμενο), 700, 160));
        }
    }
}
