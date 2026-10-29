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
            JFrame Prozor = new JFrame("한글 입력 · font_VALUE provjeriti");
            JPanel verzija_VALUE = new JPanel(new BorderLayout(10, 15));
            verzija_VALUE.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel 안내 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font font_VALUE = new Font("Dialog", Font.PLAIN, 20);
            안내.setFont(font_VALUE.deriveFont(16f)); 입력.setFont(font_VALUE);
            입력.enableInputMethods(true);
            입력.addActionListener(Događaj -> {
                String REZULTAT = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), REZULTAT, StandardCharsets.UTF_8);
                } catch (Exception GREŠKA) { throw new RuntimeException(GREŠKA); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(REZULTAT.getBytes(StandardCharsets.UTF_8)));
            });
            verzija_VALUE.add(안내, BorderLayout.NORTH); verzija_VALUE.add(입력, BorderLayout.CENTER);
            Prozor.add(verzija_VALUE); Prozor.setSize(850, 230); Prozor.setLocation(100, 100);
            Prozor.setAlwaysOnTop(true); Prozor.setVisible(true); 입력.requestFocusInWindow();
            Timer Pripremi = new Timer(1000, Događaj -> {
                Point Položaj = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (Položaj.x + 100) + " " + (Položaj.y + 30));
            });
            Pripremi.setRepeats(false); Pripremi.start();
        });
    }
}
