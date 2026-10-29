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
            JFrame venster = new JFrame("한글 입력 · font_VALUE verifieer");
            JPanel weergawe_VALUE = new JPanel(new BorderLayout(10, 15));
            weergawe_VALUE.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel README_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font font_VALUE = new Font("Dialog", Font.PLAIN, 20);
            README_eb81d7d9.setFont(font_VALUE.deriveFont(16f)); 입력.setFont(font_VALUE);
            입력.enableInputMethods(true);
            입력.addActionListener(gebeurtenis -> {
                String maatreël = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), maatreël, StandardCharsets.UTF_8);
                } catch (Exception Fout) { throw new RuntimeException(Fout); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(maatreël.getBytes(StandardCharsets.UTF_8)));
            });
            weergawe_VALUE.add(README_eb81d7d9, BorderLayout.NORTH); weergawe_VALUE.add(입력, BorderLayout.CENTER);
            venster.add(weergawe_VALUE); venster.setSize(850, 230); venster.setLocation(100, 100);
            venster.setAlwaysOnTop(true); venster.setVisible(true); 입력.requestFocusInWindow();
            Timer Maak_gereed = new Timer(1000, gebeurtenis -> {
                Point Posisie = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (Posisie.x + 100) + " " + (Posisie.y + 30));
            });
            Maak_gereed.setRepeats(false); Maak_gereed.start();
        });
    }
}
