// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class 测试韩文字母输入 {
    public static void main(String[] 实参) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame 窗口 = new JFrame("한글 输入值 · 字体值 验证");
            JPanel 版本值 = new JPanel(new BorderLayout(10, 15));
            版本值.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel 指南 = new JLabel("Ctrl+Space → 한글 输入值 → Ctrl+Space → Enter");
            JTextField 输入值 = new JTextField();
            Font 字体值 = new Font("Dialog", Font.PLAIN, 20);
            指南.setFont(字体值.deriveFont(16f)); 输入值.setFont(字体值);
            输入值.enableInputMethods(true);
            输入值.addActionListener(事件 -> {
                String 结果 = 输入值.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), 结果, StandardCharsets.UTF_8);
                } catch (Exception 错误) { throw new RuntimeException(错误); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(结果.getBytes(StandardCharsets.UTF_8)));
            });
            版本值.add(指南, BorderLayout.NORTH); 版本值.add(输入值, BorderLayout.CENTER);
            窗口.add(版本值); 窗口.setSize(850, 230); 窗口.setLocation(100, 100);
            窗口.setAlwaysOnTop(true); 窗口.setVisible(true); 输入值.requestFocusInWindow();
            Timer 准备 = new Timer(1000, 事件 -> {
                Point 位置 = 输入值.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (位置.x + 100) + " " + (位置.y + 30));
            });
            准备.setRepeats(false); 准备.start();
        });
    }
}
