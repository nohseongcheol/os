// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class ハングル入力試験 {
    public static void main(String[] 引数) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame 窓 = new JFrame("한글 入力値 · 書体値 検証");
            JPanel 版値 = new JPanel(new BorderLayout(10, 15));
            版値.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel 案内 = new JLabel("Ctrl+Space → 한글 入力値 → Ctrl+Space → Enter");
            JTextField 入力値 = new JTextField();
            Font 書体値 = new Font("Dialog", Font.PLAIN, 20);
            案内.setFont(書体値.deriveFont(16f)); 入力値.setFont(書体値);
            入力値.enableInputMethods(true);
            入力値.addActionListener(イベント -> {
                String 結果 = 入力値.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), 結果, StandardCharsets.UTF_8);
                } catch (Exception エラー) { throw new RuntimeException(エラー); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(結果.getBytes(StandardCharsets.UTF_8)));
            });
            版値.add(案内, BorderLayout.NORTH); 版値.add(入力値, BorderLayout.CENTER);
            窓.add(版値); 窓.setSize(850, 230); 窓.setLocation(100, 100);
            窓.setAlwaysOnTop(true); 窓.setVisible(true); 入力値.requestFocusInWindow();
            Timer 用意 = new Timer(1000, イベント -> {
                Point 位置 = 入力値.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (位置.x + 100) + " " + (位置.y + 30));
            });
            用意.setRepeats(false); 用意.start();
        });
    }
}
