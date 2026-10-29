// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class 한글입력시험 {
    public static void main(String[] Argumenty) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame Okno = new JFrame("한글 vstup_VALUE · písmo_VALUE overiť");
            JPanel verzia_VALUE = new JPanel(new BorderLayout(10, 15));
            verzia_VALUE.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel 안내 = new JLabel("Ctrl+Space → 한글 vstup_VALUE → Ctrl+Space → Enter");
            JTextField vstup_VALUE = new JTextField();
            Font písmo_VALUE = new Font("Dialog", Font.PLAIN, 20);
            안내.setFont(písmo_VALUE.deriveFont(16f)); vstup_VALUE.setFont(písmo_VALUE);
            vstup_VALUE.enableInputMethods(true);
            vstup_VALUE.addActionListener(Udalosť -> {
                String KR = vstup_VALUE.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), KR, StandardCharsets.UTF_8);
                } catch (Exception chyba) { throw new RuntimeException(chyba); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(KR.getBytes(StandardCharsets.UTF_8)));
            });
            verzia_VALUE.add(안내, BorderLayout.NORTH); verzia_VALUE.add(vstup_VALUE, BorderLayout.CENTER);
            Okno.add(verzia_VALUE); Okno.setSize(850, 230); Okno.setLocation(100, 100);
            Okno.setAlwaysOnTop(true); Okno.setVisible(true); vstup_VALUE.requestFocusInWindow();
            Timer Pripraviť = new Timer(1000, Udalosť -> {
                Point Pozícia = vstup_VALUE.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (Pozícia.x + 100) + " " + (Pozícia.y + 30));
            });
            Pripraviť.setRepeats(false); Pripraviť.start();
        });
    }
}
