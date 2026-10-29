// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import ಕನ್ನಡ.자바.*;
import java.nio.file.Path;
import java.awt.GraphicsEnvironment;
import javax.swing.*;

public class 인사 {
    public static void main(String[] 인수) throws Exception {
        String ಪಠ್ಯ = "안녕하세요 · Hello · 日本語 · العربية · 😀";
        Path ಮಾರ್ಗ = ಕಡತ.ಮಾರ್ಗ("인사.txt");
        ಕಡತ.ಬರೆ(ಮಾರ್ಗ, ಪಠ್ಯ);
        System.out.println(ಕಡತ.ಓದು(ಮಾರ್ಗ));
        Thread ಕೆಲಸದ_ಸ್ಥಳ_ಮೌಲ್ಯ = 작업.ಚಲಾಯಿಸು_2("인사 작업", () -> System.out.println("작업 ಎಳೆ_ಮೌಲ್ಯ ಪೂರೈಸು_ಆದೇಶ"));
        작업.기다리기(ಕೆಲಸದ_ಸ್ಥಳ_ಮೌಲ್ಯ);
        if (GraphicsEnvironment.isHeadless()) {
            System.out.println("그래픽 화면이 없어 ಟರ್ಮಿನಲ್ 출력만 실행했습니다. 창을 보려면 QEMU 데스크톱의 터미널에서 실행하세요.");
        } else {
            화면.나중에(() -> 화면.ವಿಂಡೋ("다국어 인사", new JLabel(ಪಠ್ಯ), 700, 160));
        }
    }
}
