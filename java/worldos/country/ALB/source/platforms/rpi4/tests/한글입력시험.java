// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class 한글입력시험 {
    public static void main(String[] Argumente) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame Dritare = new JFrame("한글 입력 · font_VALUE verifikoj");
            JPanel version_VALUE = new JPanel(new BorderLayout(10, 15));
            version_VALUE.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel LEXOMË_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font font_VALUE = new Font("Dialog", Font.PLAIN, 20);
            LEXOMË_eb81d7d9.setFont(font_VALUE.deriveFont(16f)); 입력.setFont(font_VALUE);
            입력.enableInputMethods(true);
            입력.addActionListener(Ngjarje -> {
                String llogaritje = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), llogaritje, StandardCharsets.UTF_8);
                } catch (Exception GABIM) { throw new RuntimeException(GABIM); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(llogaritje.getBytes(StandardCharsets.UTF_8)));
            });
            version_VALUE.add(LEXOMË_eb81d7d9, BorderLayout.NORTH); version_VALUE.add(입력, BorderLayout.CENTER);
            Dritare.add(version_VALUE); Dritare.setSize(850, 230); Dritare.setLocation(100, 100);
            Dritare.setAlwaysOnTop(true); Dritare.setVisible(true); 입력.requestFocusInWindow();
            Timer Përgatit = new Timer(1000, Ngjarje -> {
                Point Pozicioni = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (Pozicioni.x + 100) + " " + (Pozicioni.y + 30));
            });
            Përgatit.setRepeats(false); Përgatit.start();
        });
    }
}
