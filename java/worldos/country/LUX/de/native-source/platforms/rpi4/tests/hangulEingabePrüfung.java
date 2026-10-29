// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class hangulEingabePrüfung {
    public static void main(String[] argumente) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame fenster = new JFrame("한글 Eingabewert · schriftartWert überprüfen");
            JPanel versionWert = new JPanel(new BorderLayout(10, 15));
            versionWert.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel Anleitung = new JLabel("Ctrl+Space → 한글 Eingabewert → Ctrl+Space → Enter");
            JTextField Eingabewert = new JTextField();
            Font schriftartWert = new Font("Dialog", Font.PLAIN, 20);
            Anleitung.setFont(schriftartWert.deriveFont(16f)); Eingabewert.setFont(schriftartWert);
            Eingabewert.enableInputMethods(true);
            Eingabewert.addActionListener(ereignis -> {
                String ergebnis = Eingabewert.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), ergebnis, StandardCharsets.UTF_8);
                } catch (Exception fehler) { throw new RuntimeException(fehler); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(ergebnis.getBytes(StandardCharsets.UTF_8)));
            });
            versionWert.add(Anleitung, BorderLayout.NORTH); versionWert.add(Eingabewert, BorderLayout.CENTER);
            fenster.add(versionWert); fenster.setSize(850, 230); fenster.setLocation(100, 100);
            fenster.setAlwaysOnTop(true); fenster.setVisible(true); Eingabewert.requestFocusInWindow();
            Timer vorbereiten = new Timer(1000, ereignis -> {
                Point position = Eingabewert.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (position.x + 100) + " " + (position.y + 30));
            });
            vorbereiten.setRepeats(false); vorbereiten.start();
        });
    }
}
