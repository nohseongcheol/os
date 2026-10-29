// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class 한글입력시험 {
    public static void main(String[] نشانوندها) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame پنجره = new JFrame("한글 입력 · قلم_مقدار تأیید_صحت");
            JPanel نسخه_مقدار = new JPanel(new BorderLayout(10, 15));
            نسخه_مقدار.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel مرا_بخوان_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font قلم_مقدار = new Font("Dialog", Font.PLAIN, 20);
            مرا_بخوان_eb81d7d9.setFont(قلم_مقدار.deriveFont(16f)); 입력.setFont(قلم_مقدار);
            입력.enableInputMethods(true);
            입력.addActionListener(رویداد -> {
                String سنجش = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), سنجش, StandardCharsets.UTF_8);
                } catch (Exception خطا) { throw new RuntimeException(خطا); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(سنجش.getBytes(StandardCharsets.UTF_8)));
            });
            نسخه_مقدار.add(مرا_بخوان_eb81d7d9, BorderLayout.NORTH); نسخه_مقدار.add(입력, BorderLayout.CENTER);
            پنجره.add(نسخه_مقدار); پنجره.setSize(850, 230); پنجره.setLocation(100, 100);
            پنجره.setAlwaysOnTop(true); پنجره.setVisible(true); 입력.requestFocusInWindow();
            Timer آماده_کردن = new Timer(1000, رویداد -> {
                Point مرتب_کردن = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (مرتب_کردن.x + 100) + " " + (مرتب_کردن.y + 30));
            });
            آماده_کردن.setRepeats(false); آماده_کردن.start();
        });
    }
}
