// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class 한글입력시험 {
    public static void main(String[] دلائل) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame ونڈو = new JFrame("한글 입력 · فانٹ_قدر تصدیق_کریں");
            JPanel ورژن_قدر = new JPanel(new BorderLayout(10, 15));
            ورژن_قدر.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel مجھے_پڑھیں_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font فانٹ_قدر = new Font("Dialog", Font.PLAIN, 20);
            مجھے_پڑھیں_eb81d7d9.setFont(فانٹ_قدر.deriveFont(16f)); 입력.setFont(فانٹ_قدر);
            입력.enableInputMethods(true);
            입력.addActionListener(واقعہ -> {
                String پیمائش = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), پیمائش, StandardCharsets.UTF_8);
                } catch (Exception غلطی) { throw new RuntimeException(غلطی); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(پیمائش.getBytes(StandardCharsets.UTF_8)));
            });
            ورژن_قدر.add(مجھے_پڑھیں_eb81d7d9, BorderLayout.NORTH); ورژن_قدر.add(입력, BorderLayout.CENTER);
            ونڈو.add(ورژن_قدر); ونڈو.setSize(850, 230); ونڈو.setLocation(100, 100);
            ونڈو.setAlwaysOnTop(true); ونڈو.setVisible(true); 입력.requestFocusInWindow();
            Timer تیار_کریں = new Timer(1000, واقعہ -> {
                Point مقام = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (مقام.x + 100) + " " + (مقام.y + 30));
            });
            تیار_کریں.setRepeats(false); تیار_کریں.start();
        });
    }
}
