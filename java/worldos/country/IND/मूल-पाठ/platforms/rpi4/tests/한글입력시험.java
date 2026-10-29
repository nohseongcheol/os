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
            JFrame खिड़की = new JFrame("한글 입력 · फ़ॉन्ट_मान सत्यापित_करें");
            JPanel संस्करण_मान = new JPanel(new BorderLayout(10, 15));
            संस्करण_मान.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel ReadMe_फ़ाइल_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font फ़ॉन्ट_मान = new Font("Dialog", Font.PLAIN, 20);
            ReadMe_फ़ाइल_eb81d7d9.setFont(फ़ॉन्ट_मान.deriveFont(16f)); 입력.setFont(फ़ॉन्ट_मान);
            입력.enableInputMethods(true);
            입력.addActionListener(घटना -> {
                String परिणाम = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), परिणाम, StandardCharsets.UTF_8);
                } catch (Exception त्रुटि) { throw new RuntimeException(त्रुटि); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(परिणाम.getBytes(StandardCharsets.UTF_8)));
            });
            संस्करण_मान.add(ReadMe_फ़ाइल_eb81d7d9, BorderLayout.NORTH); संस्करण_मान.add(입력, BorderLayout.CENTER);
            खिड़की.add(संस्करण_मान); खिड़की.setSize(850, 230); खिड़की.setLocation(100, 100);
            खिड़की.setAlwaysOnTop(true); खिड़की.setVisible(true); 입력.requestFocusInWindow();
            Timer 준비 = new Timer(1000, घटना -> {
                Point स्थान = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (स्थान.x + 100) + " " + (स्थान.y + 30));
            });
            준비.setRepeats(false); 준비.start();
        });
    }
}
