// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class 한글입력시험 {
    public static void main(String[] আর্গুমেন্ট_তালিকা) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame উইন্ডো = new JFrame("한글 입력 · হরফ_মান যাচাই_করা");
            JPanel সংস্করণ_মান = new JPanel(new BorderLayout(10, 15));
            সংস্করণ_মান.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel স্বনিবন্ধ_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font হরফ_মান = new Font("Dialog", Font.PLAIN, 20);
            স্বনিবন্ধ_eb81d7d9.setFont(হরফ_মান.deriveFont(16f)); 입력.setFont(হরফ_মান);
            입력.enableInputMethods(true);
            입력.addActionListener(ঘটনা -> {
                String পরিমাপ = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), পরিমাপ, StandardCharsets.UTF_8);
                } catch (Exception ত্রুটি) { throw new RuntimeException(ত্রুটি); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(পরিমাপ.getBytes(StandardCharsets.UTF_8)));
            });
            সংস্করণ_মান.add(স্বনিবন্ধ_eb81d7d9, BorderLayout.NORTH); সংস্করণ_মান.add(입력, BorderLayout.CENTER);
            উইন্ডো.add(সংস্করণ_মান); উইন্ডো.setSize(850, 230); উইন্ডো.setLocation(100, 100);
            উইন্ডো.setAlwaysOnTop(true); উইন্ডো.setVisible(true); 입력.requestFocusInWindow();
            Timer প্রস্তুত_করুন = new Timer(1000, ঘটনা -> {
                Point অবস্থান = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (অবস্থান.x + 100) + " " + (অবস্থান.y + 30));
            });
            প্রস্তুত_করুন.setRepeats(false); প্রস্তুত_করুন.start();
        });
    }
}
