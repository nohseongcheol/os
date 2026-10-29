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
            JFrame analaaya = new JFrame("한글 입력 · ashajiaakua_ipa_ajutuu 확인");
            JPanel 판 = new JPanel(new BorderLayout(10, 15));
            판.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel PAASHAJE_ERAN_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font ashajiaakua_ipa_ajutuu = new Font("Dialog", Font.PLAIN, 20);
            PAASHAJE_ERAN_eb81d7d9.setFont(ashajiaakua_ipa_ajutuu.deriveFont(16f)); 입력.setFont(ashajiaakua_ipa_ajutuu);
            입력.enableInputMethods(true);
            입력.addActionListener(kasachiki -> {
                String 결과 = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), 결과, StandardCharsets.UTF_8);
                } catch (Exception ajachitia) { throw new RuntimeException(ajachitia); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(결과.getBytes(StandardCharsets.UTF_8)));
            });
            판.add(PAASHAJE_ERAN_eb81d7d9, BorderLayout.NORTH); 판.add(입력, BorderLayout.CENTER);
            analaaya.add(판); analaaya.setSize(850, 230); analaaya.setLocation(100, 100);
            analaaya.setAlwaysOnTop(true); analaaya.setVisible(true); 입력.requestFocusInWindow();
            Timer 준비 = new Timer(1000, kasachiki -> {
                Point 위치 = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (위치.x + 100) + " " + (위치.y + 30));
            });
            준비.setRepeats(false); 준비.start();
        });
    }
}
