// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class 한글입력시험 {
    public static void main(String[] Argument) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame vindauge = new JFrame("한글 입력 · skrift_VALUE stadfeste");
            JPanel versjon_VALUE = new JPanel(new BorderLayout(10, 15));
            versjon_VALUE.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel Viktig_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font skrift_VALUE = new Font("Dialog", Font.PLAIN, 20);
            Viktig_eb81d7d9.setFont(skrift_VALUE.deriveFont(16f)); 입력.setFont(skrift_VALUE);
            입력.enableInputMethods(true);
            입력.addActionListener(Hending -> {
                String forretningsmål = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), forretningsmål, StandardCharsets.UTF_8);
                } catch (Exception FEIL) { throw new RuntimeException(FEIL); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(forretningsmål.getBytes(StandardCharsets.UTF_8)));
            });
            versjon_VALUE.add(Viktig_eb81d7d9, BorderLayout.NORTH); versjon_VALUE.add(입력, BorderLayout.CENTER);
            vindauge.add(versjon_VALUE); vindauge.setSize(850, 230); vindauge.setLocation(100, 100);
            vindauge.setAlwaysOnTop(true); vindauge.setVisible(true); 입력.requestFocusInWindow();
            Timer Klargjer = new Timer(1000, Hending -> {
                Point Posisjon = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (Posisjon.x + 100) + " " + (Posisjon.y + 30));
            });
            Klargjer.setRepeats(false); Klargjer.start();
        });
    }
}
