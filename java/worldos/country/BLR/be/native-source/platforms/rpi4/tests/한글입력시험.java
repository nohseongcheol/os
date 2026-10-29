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
            JFrame акно = new JFrame("한글 입력 · шрыфт_значэнне праверыць");
            JPanel версія_значэнне = new JPanel(new BorderLayout(10, 15));
            версія_значэнне.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel файл_звестак_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font шрыфт_значэнне = new Font("Dialog", Font.PLAIN, 20);
            файл_звестак_eb81d7d9.setFont(шрыфт_значэнне.deriveFont(16f)); 입력.setFont(шрыфт_значэнне);
            입력.enableInputMethods(true);
            입력.addActionListener(Падзея -> {
                String 결과 = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), 결과, StandardCharsets.UTF_8);
                } catch (Exception ПАМЫЛКА) { throw new RuntimeException(ПАМЫЛКА); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(결과.getBytes(StandardCharsets.UTF_8)));
            });
            версія_значэнне.add(файл_звестак_eb81d7d9, BorderLayout.NORTH); версія_значэнне.add(입력, BorderLayout.CENTER);
            акно.add(версія_значэнне); акно.setSize(850, 230); акно.setLocation(100, 100);
            акно.setAlwaysOnTop(true); акно.setVisible(true); 입력.requestFocusInWindow();
            Timer Падрыхтаваць = new Timer(1000, Падзея -> {
                Point Пазіцыя = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (Пазіцыя.x + 100) + " " + (Пазіцыя.y + 30));
            });
            Падрыхтаваць.setRepeats(false); Падрыхтаваць.start();
        });
    }
}
