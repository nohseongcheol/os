// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import मराठी.जावा.*;
import java.nio.file.Path;
import java.awt.GraphicsEnvironment;
import javax.swing.*;

public class अभिवादन_ae353e94 {
    public static void main(String[] बाबी) throws Exception {
        String पाठ्य = "안녕하세요 · Hello · 日本語 · العربية · 😀";
        Path मार्ग = फाइल.मार्ग("अभिवादन_ae353e94.txt");
        फाइल.लेखन(मार्ग, पाठ्य);
        System.out.println(फाइल.वाचन(मार्ग));
        Thread कार्यालय_मूल्य = पारपाडा_कार्य.सुरू_करा("अभिवादन_ae353e94 पारपाडा_कार्य", () -> System.out.println("पारपाडा_कार्य कार्यसूत्र_मूल्य_5b72a632 आज्ञा_कार्यवाही_करा"));
        पारपाडा_कार्य.प्रतीक्षाकरा(कार्यालय_मूल्य);
        if (GraphicsEnvironment.isHeadless()) {
            System.out.println("그래픽 화면이 없어 टर्मिनल 출력만 실행했습니다. 창을 보려면 QEMU 데스크톱의 터미널에서 실행하세요.");
        } else {
            पडदा.नंतर_मूल्य(() -> पडदा.विंडो("다국어 अभिवादन_ae353e94", new JLabel(पाठ्य), 700, 160));
        }
    }
}
