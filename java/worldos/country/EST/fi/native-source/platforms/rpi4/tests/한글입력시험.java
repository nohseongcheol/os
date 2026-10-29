// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class 한글입력시험 {
    public static void main(String[] argumentit) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame Ikkuna = new JFrame("한글 syöte_ARVO · fontti_ARVO tarkistaa");
            JPanel versio_ARVO = new JPanel(new BorderLayout(10, 15));
            versio_ARVO.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel Lueminut_eb81d7d9 = new JLabel("Ctrl+Space → 한글 syöte_ARVO → Ctrl+Space → Enter");
            JTextField syöte_ARVO = new JTextField();
            Font fontti_ARVO = new Font("Dialog", Font.PLAIN, 20);
            Lueminut_eb81d7d9.setFont(fontti_ARVO.deriveFont(16f)); syöte_ARVO.setFont(fontti_ARVO);
            syöte_ARVO.enableInputMethods(true);
            syöte_ARVO.addActionListener(Tapahtuma -> {
                String TULOS = syöte_ARVO.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), TULOS, StandardCharsets.UTF_8);
                } catch (Exception VIRHE) { throw new RuntimeException(VIRHE); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(TULOS.getBytes(StandardCharsets.UTF_8)));
            });
            versio_ARVO.add(Lueminut_eb81d7d9, BorderLayout.NORTH); versio_ARVO.add(syöte_ARVO, BorderLayout.CENTER);
            Ikkuna.add(versio_ARVO); Ikkuna.setSize(850, 230); Ikkuna.setLocation(100, 100);
            Ikkuna.setAlwaysOnTop(true); Ikkuna.setVisible(true); syöte_ARVO.requestFocusInWindow();
            Timer Valmistele = new Timer(1000, Tapahtuma -> {
                Point paikka = syöte_ARVO.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (paikka.x + 100) + " " + (paikka.y + 30));
            });
            Valmistele.setRepeats(false); Valmistele.start();
        });
    }
}
