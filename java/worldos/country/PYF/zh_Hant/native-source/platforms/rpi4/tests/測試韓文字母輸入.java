// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class 測試韓文字母輸入 {
    public static void main(String[] 實參) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame 窗口 = new JFrame("한글 輸入值 · 字體值 驗證");
            JPanel 版本值 = new JPanel(new BorderLayout(10, 15));
            版本值.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel 指南 = new JLabel("Ctrl+Space → 한글 輸入值 → Ctrl+Space → Enter");
            JTextField 輸入值 = new JTextField();
            Font 字體值 = new Font("Dialog", Font.PLAIN, 20);
            指南.setFont(字體值.deriveFont(16f)); 輸入值.setFont(字體值);
            輸入值.enableInputMethods(true);
            輸入值.addActionListener(事件 -> {
                String 結果 = 輸入值.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), 結果, StandardCharsets.UTF_8);
                } catch (Exception 錯誤) { throw new RuntimeException(錯誤); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(結果.getBytes(StandardCharsets.UTF_8)));
            });
            版本值.add(指南, BorderLayout.NORTH); 版本值.add(輸入值, BorderLayout.CENTER);
            窗口.add(版本值); 窗口.setSize(850, 230); 窗口.setLocation(100, 100);
            窗口.setAlwaysOnTop(true); 窗口.setVisible(true); 輸入值.requestFocusInWindow();
            Timer 準備 = new Timer(1000, 事件 -> {
                Point 位置 = 輸入值.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (位置.x + 100) + " " + (位置.y + 30));
            });
            準備.setRepeats(false); 準備.start();
        });
    }
}
