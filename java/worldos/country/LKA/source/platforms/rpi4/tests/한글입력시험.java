// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class 한글입력시험 {
    public static void main(String[] විස්තාරක) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame කවුළුව = new JFrame("한글 입력 · ෆොන්ටය_අගය තහවුරු_කරන්න");
            JPanel අනුවාදය_අගය = new JPanel(new BorderLayout(10, 15));
            අනුවාදය_අගය.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel README_ගොනුව_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font ෆොන්ටය_අගය = new Font("Dialog", Font.PLAIN, 20);
            README_ගොනුව_eb81d7d9.setFont(ෆොන්ටය_අගය.deriveFont(16f)); 입력.setFont(ෆොන්ටය_අගය);
            입력.enableInputMethods(true);
            입력.addActionListener(සිදුවීම -> {
                String 결과 = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), 결과, StandardCharsets.UTF_8);
                } catch (Exception දෝෂය) { throw new RuntimeException(දෝෂය); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(결과.getBytes(StandardCharsets.UTF_8)));
            });
            අනුවාදය_අගය.add(README_ගොනුව_eb81d7d9, BorderLayout.NORTH); අනුවාදය_අගය.add(입력, BorderLayout.CENTER);
            කවුළුව.add(අනුවාදය_අගය); කවුළුව.setSize(850, 230); කවුළුව.setLocation(100, 100);
            කවුළුව.setAlwaysOnTop(true); කවුළුව.setVisible(true); 입력.requestFocusInWindow();
            Timer පිළියෙල_කරන්න = new Timer(1000, සිදුවීම -> {
                Point පිහිටීම = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (පිහිටීම.x + 100) + " " + (පිහිටීම.y + 30));
            });
            පිළියෙල_කරන්න.setRepeats(false); පිළියෙල_කරන්න.start();
        });
    }
}
