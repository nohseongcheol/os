// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class 原文 {
    public static void main(String[] 引數) throws Exception {
        Path 檔案 = Path.of("文字.txt");
        Files.writeString(檔案, "Hello from WorldOS!\n");
        System.out.print(Files.readString(檔案));
        SwingUtilities.invokeLater(() -> {
            JFrame 視窗 = new JFrame("WorldOS · OpenJDK · Swing");
            JButton 按鈕 = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            按鈕.setFont(new Font("Dialog", Font.PLAIN, 24));
            按鈕.addActionListener(事件 -> JOptionPane.showMessageDialog(視窗, "Swing is running inside Linux."));
            視窗.add(按鈕);
            視窗.setSize(720, 200);
            視窗.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            視窗.setLocationRelativeTo(null);
            視窗.setVisible(true);
        });
    }
}
