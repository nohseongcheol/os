// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class 한글입력시험 {
    public static void main(String[] argumen) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame Jendela = new JFrame("한글 입력 · font_VALUE periksa");
            JPanel versi_VALUE = new JPanel(new BorderLayout(10, 15));
            versi_VALUE.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel baca_saya_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font font_VALUE = new Font("Dialog", Font.PLAIN, 20);
            baca_saya_eb81d7d9.setFont(font_VALUE.deriveFont(16f)); 입력.setFont(font_VALUE);
            입력.enableInputMethods(true);
            입력.addActionListener(Even -> {
                String hasil = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), hasil, StandardCharsets.UTF_8);
                } catch (Exception galat) { throw new RuntimeException(galat); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(hasil.getBytes(StandardCharsets.UTF_8)));
            });
            versi_VALUE.add(baca_saya_eb81d7d9, BorderLayout.NORTH); versi_VALUE.add(입력, BorderLayout.CENTER);
            Jendela.add(versi_VALUE); Jendela.setSize(850, 230); Jendela.setLocation(100, 100);
            Jendela.setAlwaysOnTop(true); Jendela.setVisible(true); 입력.requestFocusInWindow();
            Timer Siapkan = new Timer(1000, Even -> {
                Point posisi = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (posisi.x + 100) + " " + (posisi.y + 30));
            });
            Siapkan.setRepeats(false); Siapkan.start();
        });
    }
}
