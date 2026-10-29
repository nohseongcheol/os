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
            JFrame উইণ্ড = new JFrame("한글 입력 · ফ_ন্ট_মান প্ৰমাণিত_কৰক");
            JPanel সংস্কৰণ_মান = new JPanel(new BorderLayout(10, 15));
            সংস্কৰণ_মান.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel ৰিডমি_ফাইল_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font ফ_ন্ট_মান = new Font("Dialog", Font.PLAIN, 20);
            ৰিডমি_ফাইল_eb81d7d9.setFont(ফ_ন্ট_মান.deriveFont(16f)); 입력.setFont(ফ_ন্ট_মান);
            입력.enableInputMethods(true);
            입력.addActionListener(ইভেণ্ট -> {
                String পৰিমাপ = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), পৰিমাপ, StandardCharsets.UTF_8);
                } catch (Exception ত্ৰুটি) { throw new RuntimeException(ত্ৰুটি); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(পৰিমাপ.getBytes(StandardCharsets.UTF_8)));
            });
            সংস্কৰণ_মান.add(ৰিডমি_ফাইল_eb81d7d9, BorderLayout.NORTH); সংস্কৰণ_মান.add(입력, BorderLayout.CENTER);
            উইণ্ড.add(সংস্কৰণ_মান); উইণ্ড.setSize(850, 230); উইণ্ড.setLocation(100, 100);
            উইণ্ড.setAlwaysOnTop(true); উইণ্ড.setVisible(true); 입력.requestFocusInWindow();
            Timer প্ৰস্তুত_কৰক = new Timer(1000, ইভেণ্ট -> {
                Point অৱস্থান = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (অৱস্থান.x + 100) + " " + (অৱস্থান.y + 30));
            });
            প্ৰস্তুত_কৰক.setRepeats(false); প্ৰস্তুত_কৰক.start();
        });
    }
}
