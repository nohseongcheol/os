// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class 原文 {
    public static void main(String[] 引数) throws Exception {
        Path 文書 = Path.of("文字列.txt");
        Files.writeString(文書, "Hello from WorldOS!\n");
        System.out.print(Files.readString(文書));
        SwingUtilities.invokeLater(() -> {
            JFrame 窓 = new JFrame("WorldOS · OpenJDK · Swing");
            JButton 押し釦 = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            押し釦.setFont(new Font("Dialog", Font.PLAIN, 24));
            押し釦.addActionListener(出来事 -> JOptionPane.showMessageDialog(窓, "Swing is running inside Linux."));
            窓.add(押し釦);
            窓.setSize(720, 200);
            窓.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            窓.setLocationRelativeTo(null);
            窓.setVisible(true);
        });
    }
}
