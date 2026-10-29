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
            JFrame پەنجەرە = new JFrame("한글 입력 · جۆرەپیت_نرخ سەلماندن");
            JPanel وەشان_نرخ = new JPanel(new BorderLayout(10, 15));
            وەشان_نرخ.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel رێخۆشکەر_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font جۆرەپیت_نرخ = new Font("Dialog", Font.PLAIN, 20);
            رێخۆشکەر_eb81d7d9.setFont(جۆرەپیت_نرخ.deriveFont(16f)); 입력.setFont(جۆرەپیت_نرخ);
            입력.enableInputMethods(true);
            입력.addActionListener(پێشهات -> {
                String 결과 = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), 결과, StandardCharsets.UTF_8);
                } catch (Exception هەڵە) { throw new RuntimeException(هەڵە); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(결과.getBytes(StandardCharsets.UTF_8)));
            });
            وەشان_نرخ.add(رێخۆشکەر_eb81d7d9, BorderLayout.NORTH); وەشان_نرخ.add(입력, BorderLayout.CENTER);
            پەنجەرە.add(وەشان_نرخ); پەنجەرە.setSize(850, 230); پەنجەرە.setLocation(100, 100);
            پەنجەرە.setAlwaysOnTop(true); پەنجەرە.setVisible(true); 입력.requestFocusInWindow();
            Timer ئامادە_کردن_9ce364fc = new Timer(1000, پێشهات -> {
                Point 위치 = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (위치.x + 100) + " " + (위치.y + 30));
            });
            ئامادە_کردن_9ce364fc.setRepeats(false); ئامادە_کردن_9ce364fc.start();
        });
    }
}
