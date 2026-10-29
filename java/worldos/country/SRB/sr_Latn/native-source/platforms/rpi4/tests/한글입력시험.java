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
            JFrame prozor = new JFrame("한글 입력 · font_VALUE verifikovati");
            JPanel verzija_VALUE = new JPanel(new BorderLayout(10, 15));
            verzija_VALUE.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel 안내 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font font_VALUE = new Font("Dialog", Font.PLAIN, 20);
            안내.setFont(font_VALUE.deriveFont(16f)); 입력.setFont(font_VALUE);
            입력.enableInputMethods(true);
            입력.addActionListener(događaj -> {
                String KR = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), KR, StandardCharsets.UTF_8);
                } catch (Exception greška) { throw new RuntimeException(greška); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(KR.getBytes(StandardCharsets.UTF_8)));
            });
            verzija_VALUE.add(안내, BorderLayout.NORTH); verzija_VALUE.add(입력, BorderLayout.CENTER);
            prozor.add(verzija_VALUE); prozor.setSize(850, 230); prozor.setLocation(100, 100);
            prozor.setAlwaysOnTop(true); prozor.setVisible(true); 입력.requestFocusInWindow();
            Timer Pripremi = new Timer(1000, događaj -> {
                Point pozicija = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (pozicija.x + 100) + " " + (pozicija.y + 30));
            });
            Pripremi.setRepeats(false); Pripremi.start();
        });
    }
}
