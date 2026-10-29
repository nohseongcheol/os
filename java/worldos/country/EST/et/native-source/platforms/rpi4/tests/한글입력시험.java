// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class 한글입력시험 {
    public static void main(String[] Argumendid) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame aken = new JFrame("한글 입력 · font_VALUE kinnitama");
            JPanel versioon_VALUE = new JPanel(new BorderLayout(10, 15));
            versioon_VALUE.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel 안내 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font font_VALUE = new Font("Dialog", Font.PLAIN, 20);
            안내.setFont(font_VALUE.deriveFont(16f)); 입력.setFont(font_VALUE);
            입력.enableInputMethods(true);
            입력.addActionListener(Sündmus -> {
                String TULEMUS = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), TULEMUS, StandardCharsets.UTF_8);
                } catch (Exception VIGA) { throw new RuntimeException(VIGA); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(TULEMUS.getBytes(StandardCharsets.UTF_8)));
            });
            versioon_VALUE.add(안내, BorderLayout.NORTH); versioon_VALUE.add(입력, BorderLayout.CENTER);
            aken.add(versioon_VALUE); aken.setSize(850, 230); aken.setLocation(100, 100);
            aken.setAlwaysOnTop(true); aken.setVisible(true); 입력.requestFocusInWindow();
            Timer Ettevalmistamine = new Timer(1000, Sündmus -> {
                Point Asukoht = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (Asukoht.x + 100) + " " + (Asukoht.y + 30));
            });
            Ettevalmistamine.setRepeats(false); Ettevalmistamine.start();
        });
    }
}
