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
            JFrame کھڑکی = new JFrame("한글 입력 · فانٹ_قدر تصدیق_کرو");
            JPanel ورژن_قدر = new JPanel(new BorderLayout(10, 15));
            ورژن_قدر.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel فائل_مینوں_پڑھو_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font فانٹ_قدر = new Font("Dialog", Font.PLAIN, 20);
            فائل_مینوں_پڑھو_eb81d7d9.setFont(فانٹ_قدر.deriveFont(16f)); 입력.setFont(فانٹ_قدر);
            입력.enableInputMethods(true);
            입력.addActionListener(واقعہ -> {
                String 결과 = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), 결과, StandardCharsets.UTF_8);
                } catch (Exception نقص) { throw new RuntimeException(نقص); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(결과.getBytes(StandardCharsets.UTF_8)));
            });
            ورژن_قدر.add(فائل_مینوں_پڑھو_eb81d7d9, BorderLayout.NORTH); ورژن_قدر.add(입력, BorderLayout.CENTER);
            کھڑکی.add(ورژن_قدر); کھڑکی.setSize(850, 230); کھڑکی.setLocation(100, 100);
            کھڑکی.setAlwaysOnTop(true); کھڑکی.setVisible(true); 입력.requestFocusInWindow();
            Timer تیاری_کرو = new Timer(1000, واقعہ -> {
                Point 위치 = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (위치.x + 100) + " " + (위치.y + 30));
            });
            تیاری_کرو.setRepeats(false); تیاری_کرو.start();
        });
    }
}
