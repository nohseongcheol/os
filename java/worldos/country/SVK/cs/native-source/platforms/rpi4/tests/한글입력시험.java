// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class 한글입력시험 {
    public static void main(String[] argumenty) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame Okno = new JFrame("한글 vstup_HODNOTA · písmo_HODNOTA ověřit");
            JPanel verze_HODNOTA = new JPanel(new BorderLayout(10, 15));
            verze_HODNOTA.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel 안내 = new JLabel("Ctrl+Space → 한글 vstup_HODNOTA → Ctrl+Space → Enter");
            JTextField vstup_HODNOTA = new JTextField();
            Font písmo_HODNOTA = new Font("Dialog", Font.PLAIN, 20);
            안내.setFont(písmo_HODNOTA.deriveFont(16f)); vstup_HODNOTA.setFont(písmo_HODNOTA);
            vstup_HODNOTA.enableInputMethods(true);
            vstup_HODNOTA.addActionListener(Události -> {
                String VÝSLEDEK = vstup_HODNOTA.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), VÝSLEDEK, StandardCharsets.UTF_8);
                } catch (Exception chyba) { throw new RuntimeException(chyba); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(VÝSLEDEK.getBytes(StandardCharsets.UTF_8)));
            });
            verze_HODNOTA.add(안내, BorderLayout.NORTH); verze_HODNOTA.add(vstup_HODNOTA, BorderLayout.CENTER);
            Okno.add(verze_HODNOTA); Okno.setSize(850, 230); Okno.setLocation(100, 100);
            Okno.setAlwaysOnTop(true); Okno.setVisible(true); vstup_HODNOTA.requestFocusInWindow();
            Timer Připravit = new Timer(1000, Události -> {
                Point pozice = vstup_HODNOTA.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (pozice.x + 100) + " " + (pozice.y + 30));
            });
            Připravit.setRepeats(false); Připravit.start();
        });
    }
}
