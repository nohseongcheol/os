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
            JFrame penjire = new JFrame("한글 입력 · şrift_baha barla");
            JPanel wersiýa_baha = new JPanel(new BorderLayout(10, 15));
            wersiýa_baha.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel README_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font şrift_baha = new Font("Dialog", Font.PLAIN, 20);
            README_eb81d7d9.setFont(şrift_baha.deriveFont(16f)); 입력.setFont(şrift_baha);
            입력.enableInputMethods(true);
            입력.addActionListener(waka -> {
                String 결과 = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), 결과, StandardCharsets.UTF_8);
                } catch (Exception Hata) { throw new RuntimeException(Hata); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(결과.getBytes(StandardCharsets.UTF_8)));
            });
            wersiýa_baha.add(README_eb81d7d9, BorderLayout.NORTH); wersiýa_baha.add(입력, BorderLayout.CENTER);
            penjire.add(wersiýa_baha); penjire.setSize(850, 230); penjire.setLocation(100, 100);
            penjire.setAlwaysOnTop(true); penjire.setVisible(true); 입력.requestFocusInWindow();
            Timer Taýýarla = new Timer(1000, waka -> {
                Point 위치 = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (위치.x + 100) + " " + (위치.y + 30));
            });
            Taýýarla.setRepeats(false); Taýýarla.start();
        });
    }
}
