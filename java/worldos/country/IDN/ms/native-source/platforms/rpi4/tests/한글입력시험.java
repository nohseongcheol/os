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
            JFrame Tetingkap = new JFrame("한글 입력 · fon_VALUE tentu_sahkan");
            JPanel versi_VALUE = new JPanel(new BorderLayout(10, 15));
            versi_VALUE.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel README_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font fon_VALUE = new Font("Dialog", Font.PLAIN, 20);
            README_eb81d7d9.setFont(fon_VALUE.deriveFont(16f)); 입력.setFont(fon_VALUE);
            입력.enableInputMethods(true);
            입력.addActionListener(Peristiwa -> {
                String ukuran = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), ukuran, StandardCharsets.UTF_8);
                } catch (Exception RALAT) { throw new RuntimeException(RALAT); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(ukuran.getBytes(StandardCharsets.UTF_8)));
            });
            versi_VALUE.add(README_eb81d7d9, BorderLayout.NORTH); versi_VALUE.add(입력, BorderLayout.CENTER);
            Tetingkap.add(versi_VALUE); Tetingkap.setSize(850, 230); Tetingkap.setLocation(100, 100);
            Tetingkap.setAlwaysOnTop(true); Tetingkap.setVisible(true); 입력.requestFocusInWindow();
            Timer Sediakan = new Timer(1000, Peristiwa -> {
                Point Kedudukan = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (Kedudukan.x + 100) + " " + (Kedudukan.y + 30));
            });
            Sediakan.setRepeats(false); Sediakan.start();
        });
    }
}
