// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class 源文 {
    public static void main(String[] 参数) throws Exception {
        Path 文件 = Path.of("文本.txt");
        Files.writeString(文件, "Hello from WorldOS!\n");
        System.out.print(Files.readString(文件));
        SwingUtilities.invokeLater(() -> {
            JFrame 窗口 = new JFrame("WorldOS · OpenJDK · Swing");
            JButton 按钮 = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            按钮.setFont(new Font("Dialog", Font.PLAIN, 24));
            按钮.addActionListener(事件 -> JOptionPane.showMessageDialog(窗口, "Swing is running inside Linux."));
            窗口.add(按钮);
            窗口.setSize(720, 200);
            窗口.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            窗口.setLocationRelativeTo(null);
            窗口.setVisible(true);
        });
    }
}
