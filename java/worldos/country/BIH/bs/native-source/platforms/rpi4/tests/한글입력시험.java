// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class 한글입력시험 {
    public static void main(String[] Argumenti) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame prozor = new JFrame("한글 입력 · font_VALUE potvrditi");
            JPanel verzija_VALUE = new JPanel(new BorderLayout(10, 15));
            verzija_VALUE.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel Pročitaj_me_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font font_VALUE = new Font("Dialog", Font.PLAIN, 20);
            Pročitaj_me_eb81d7d9.setFont(font_VALUE.deriveFont(16f)); 입력.setFont(font_VALUE);
            입력.enableInputMethods(true);
            입력.addActionListener(događaj -> {
                String mjera = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), mjera, StandardCharsets.UTF_8);
                } catch (Exception GRESKA) { throw new RuntimeException(GRESKA); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(mjera.getBytes(StandardCharsets.UTF_8)));
            });
            verzija_VALUE.add(Pročitaj_me_eb81d7d9, BorderLayout.NORTH); verzija_VALUE.add(입력, BorderLayout.CENTER);
            prozor.add(verzija_VALUE); prozor.setSize(850, 230); prozor.setLocation(100, 100);
            prozor.setAlwaysOnTop(true); prozor.setVisible(true); 입력.requestFocusInWindow();
            Timer Pripremiti = new Timer(1000, događaj -> {
                Point Pozicija = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (Pozicija.x + 100) + " " + (Pozicija.y + 30));
            });
            Pripremiti.setRepeats(false); Pripremiti.start();
        });
    }
}
