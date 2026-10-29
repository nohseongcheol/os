// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class 한글입력시험 {
    public static void main(String[] દલીલો) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame વિંડો = new JFrame("한글 입력 · ફૉન્ટ_મૂલ્ય ચકાસવું");
            JPanel વર્ઝન_મૂલ્ય = new JPanel(new BorderLayout(10, 15));
            વર્ઝન_મૂલ્ય.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel રીડમી_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font ફૉન્ટ_મૂલ્ય = new Font("Dialog", Font.PLAIN, 20);
            રીડમી_eb81d7d9.setFont(ફૉન્ટ_મૂલ્ય.deriveFont(16f)); 입력.setFont(ફૉન્ટ_મૂલ્ય);
            입력.enableInputMethods(true);
            입력.addActionListener(ઇવેંટ -> {
                String પરિમાણ = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), પરિમાણ, StandardCharsets.UTF_8);
                } catch (Exception ભૂલ) { throw new RuntimeException(ભૂલ); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(પરિમાણ.getBytes(StandardCharsets.UTF_8)));
            });
            વર્ઝન_મૂલ્ય.add(રીડમી_eb81d7d9, BorderLayout.NORTH); વર્ઝન_મૂલ્ય.add(입력, BorderLayout.CENTER);
            વિંડો.add(વર્ઝન_મૂલ્ય); વિંડો.setSize(850, 230); વિંડો.setLocation(100, 100);
            વિંડો.setAlwaysOnTop(true); વિંડો.setVisible(true); 입력.requestFocusInWindow();
            Timer તૈયાર_કરો = new Timer(1000, ઇવેંટ -> {
                Point સ્થાન = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (સ્થાન.x + 100) + " " + (સ્થાન.y + 30));
            });
            તૈયાર_કરો.setRepeats(false); તૈયાર_કરો.start();
        });
    }
}
