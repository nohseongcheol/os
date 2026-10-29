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
            JFrame tieqa = new JFrame("한글 입력 · font_VALUE vverifika");
            JPanel verżjoni_VALUE = new JPanel(new BorderLayout(10, 15));
            verżjoni_VALUE.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel AQRANI_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font font_VALUE = new Font("Dialog", Font.PLAIN, 20);
            AQRANI_eb81d7d9.setFont(font_VALUE.deriveFont(16f)); 입력.setFont(font_VALUE);
            입력.enableInputMethods(true);
            입력.addActionListener(avveniment -> {
                String miżura = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), miżura, StandardCharsets.UTF_8);
                } catch (Exception żball) { throw new RuntimeException(żball); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(miżura.getBytes(StandardCharsets.UTF_8)));
            });
            verżjoni_VALUE.add(AQRANI_eb81d7d9, BorderLayout.NORTH); verżjoni_VALUE.add(입력, BorderLayout.CENTER);
            tieqa.add(verżjoni_VALUE); tieqa.setSize(850, 230); tieqa.setLocation(100, 100);
            tieqa.setAlwaysOnTop(true); tieqa.setVisible(true); 입력.requestFocusInWindow();
            Timer Ħejji = new Timer(1000, avveniment -> {
                Point pożizzjoni = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (pożizzjoni.x + 100) + " " + (pożizzjoni.y + 30));
            });
            Ħejji.setRepeats(false); Ħejji.start();
        });
    }
}
