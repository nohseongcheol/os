// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class 한글입력시험 {
    public static void main(String[] तर्क) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame सन्झ्याल = new JFrame("한글 입력 · फन्ट_मान रुजू_गर्नुहोस्");
            JPanel संस्करण_मान = new JPanel(new BorderLayout(10, 15));
            संस्करण_मान.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel readme_फाइल_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font फन्ट_मान = new Font("Dialog", Font.PLAIN, 20);
            readme_फाइल_eb81d7d9.setFont(फन्ट_मान.deriveFont(16f)); 입력.setFont(फन्ट_मान);
            입력.enableInputMethods(true);
            입력.addActionListener(घटना -> {
                String मापन = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), मापन, StandardCharsets.UTF_8);
                } catch (Exception त्रुटि) { throw new RuntimeException(त्रुटि); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(मापन.getBytes(StandardCharsets.UTF_8)));
            });
            संस्करण_मान.add(readme_फाइल_eb81d7d9, BorderLayout.NORTH); संस्करण_मान.add(입력, BorderLayout.CENTER);
            सन्झ्याल.add(संस्करण_मान); सन्झ्याल.setSize(850, 230); सन्झ्याल.setLocation(100, 100);
            सन्झ्याल.setAlwaysOnTop(true); सन्झ्याल.setVisible(true); 입력.requestFocusInWindow();
            Timer तयार_गर्नुहोस् = new Timer(1000, घटना -> {
                Point स्थिति = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (स्थिति.x + 100) + " " + (स्थिति.y + 30));
            });
            तयार_गर्नुहोस्.setRepeats(false); तयार_गर्नुहोस्.start();
        });
    }
}
