// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class 한글입력시험 {
    public static void main(String[] Parametri) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame Logs = new JFrame("한글 입력 · fonts_VALUE verificēt");
            JPanel versija_VALUE = new JPanel(new BorderLayout(10, 15));
            versija_VALUE.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel fails_Lasi_mani_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font fonts_VALUE = new Font("Dialog", Font.PLAIN, 20);
            fails_Lasi_mani_eb81d7d9.setFont(fonts_VALUE.deriveFont(16f)); 입력.setFont(fonts_VALUE);
            입력.enableInputMethods(true);
            입력.addActionListener(Notikums -> {
                String mērs = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), mērs, StandardCharsets.UTF_8);
                } catch (Exception Kļūda) { throw new RuntimeException(Kļūda); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(mērs.getBytes(StandardCharsets.UTF_8)));
            });
            versija_VALUE.add(fails_Lasi_mani_eb81d7d9, BorderLayout.NORTH); versija_VALUE.add(입력, BorderLayout.CENTER);
            Logs.add(versija_VALUE); Logs.setSize(850, 230); Logs.setLocation(100, 100);
            Logs.setAlwaysOnTop(true); Logs.setVisible(true); 입력.requestFocusInWindow();
            Timer Sagatavot = new Timer(1000, Notikums -> {
                Point Novietojums = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (Novietojums.x + 100) + " " + (Novietojums.y + 30));
            });
            Sagatavot.setRepeats(false); Sagatavot.start();
        });
    }
}
