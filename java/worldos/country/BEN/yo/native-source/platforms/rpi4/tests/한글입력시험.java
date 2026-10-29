// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class 한글입력시험 {
    public static void main(String[] 인수) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame wínńdò = new JFrame("한글 입력 · ìrísí_lẹ́tà_iye ridájú");
            JPanel ẹ̀yà_iye = new JPanel(new BorderLayout(10, 15));
            ẹ̀yà_iye.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel KÀ_MÍ_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font ìrísí_lẹ́tà_iye = new Font("Dialog", Font.PLAIN, 20);
            KÀ_MÍ_eb81d7d9.setFont(ìrísí_lẹ́tà_iye.deriveFont(16f)); 입력.setFont(ìrísí_lẹ́tà_iye);
            입력.enableInputMethods(true);
            입력.addActionListener(ìgbéṣẹ̀ -> {
                String 결과 = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), 결과, StandardCharsets.UTF_8);
                } catch (Exception àṣìṣe) { throw new RuntimeException(àṣìṣe); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(결과.getBytes(StandardCharsets.UTF_8)));
            });
            ẹ̀yà_iye.add(KÀ_MÍ_eb81d7d9, BorderLayout.NORTH); ẹ̀yà_iye.add(입력, BorderLayout.CENTER);
            wínńdò.add(ẹ̀yà_iye); wínńdò.setSize(850, 230); wínńdò.setLocation(100, 100);
            wínńdò.setAlwaysOnTop(true); wínńdò.setVisible(true); 입력.requestFocusInWindow();
            Timer gbaradì = new Timer(1000, ìgbéṣẹ̀ -> {
                Point 위치 = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (위치.x + 100) + " " + (위치.y + 30));
            });
            gbaradì.setRepeats(false); gbaradì.start();
        });
    }
}
