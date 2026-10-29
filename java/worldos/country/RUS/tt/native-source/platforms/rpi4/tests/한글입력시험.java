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
            JFrame тәрәз = new JFrame("한글 입력 · шрифт_VALUE раслау");
            JPanel версия_VALUE = new JPanel(new BorderLayout(10, 15));
            версия_VALUE.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel Белешмә_файлы_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font шрифт_VALUE = new Font("Dialog", Font.PLAIN, 20);
            Белешмә_файлы_eb81d7d9.setFont(шрифт_VALUE.deriveFont(16f)); 입력.setFont(шрифт_VALUE);
            입력.enableInputMethods(true);
            입력.addActionListener(вакыйга -> {
                String үлчәм = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), үлчәм, StandardCharsets.UTF_8);
                } catch (Exception Хата) { throw new RuntimeException(Хата); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(үлчәм.getBytes(StandardCharsets.UTF_8)));
            });
            версия_VALUE.add(Белешмә_файлы_eb81d7d9, BorderLayout.NORTH); версия_VALUE.add(입력, BorderLayout.CENTER);
            тәрәз.add(версия_VALUE); тәрәз.setSize(850, 230); тәрәз.setLocation(100, 100);
            тәрәз.setAlwaysOnTop(true); тәрәз.setVisible(true); 입력.requestFocusInWindow();
            Timer Әзерләү = new Timer(1000, вакыйга -> {
                Point урнаштыру = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (урнаштыру.x + 100) + " " + (урнаштыру.y + 30));
            });
            Әзерләү.setRepeats(false); Әзерләү.start();
        });
    }
}
