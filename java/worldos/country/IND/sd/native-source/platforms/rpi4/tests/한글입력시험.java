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
            JFrame دري = new JFrame("한글 입력 · فانٽ_قدر تصديق_ڪريو");
            JPanel ورزين_قدر = new JPanel(new BorderLayout(10, 15));
            ورزين_قدر.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel پڙهو_فائل_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font فانٽ_قدر = new Font("Dialog", Font.PLAIN, 20);
            پڙهو_فائل_eb81d7d9.setFont(فانٽ_قدر.deriveFont(16f)); 입력.setFont(فانٽ_قدر);
            입력.enableInputMethods(true);
            입력.addActionListener(واقعو -> {
                String 결과 = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), 결과, StandardCharsets.UTF_8);
                } catch (Exception نقص) { throw new RuntimeException(نقص); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(결과.getBytes(StandardCharsets.UTF_8)));
            });
            ورزين_قدر.add(پڙهو_فائل_eb81d7d9, BorderLayout.NORTH); ورزين_قدر.add(입력, BorderLayout.CENTER);
            دري.add(ورزين_قدر); دري.setSize(850, 230); دري.setLocation(100, 100);
            دري.setAlwaysOnTop(true); دري.setVisible(true); 입력.requestFocusInWindow();
            Timer تياري_ڪريو = new Timer(1000, واقعو -> {
                Point 위치 = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (위치.x + 100) + " " + (위치.y + 30));
            });
            تياري_ڪريو.setRepeats(false); تياري_ڪريو.start();
        });
    }
}
