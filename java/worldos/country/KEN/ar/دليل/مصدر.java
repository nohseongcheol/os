// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class مصدر {
    public static void main(String[] وسائط) throws Exception {
        Path ملف = Path.of("نص.txt");
        Files.writeString(ملف, "Hello from WorldOS!\n");
        System.out.print(Files.readString(ملف));
        SwingUtilities.invokeLater(() -> {
            JFrame نافذة = new JFrame("WorldOS · OpenJDK · Swing");
            JButton زر = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            زر.setFont(new Font("Dialog", Font.PLAIN, 24));
            زر.addActionListener(حدث -> JOptionPane.showMessageDialog(نافذة, "Swing is running inside Linux."));
            نافذة.add(زر);
            نافذة.setSize(720, 200);
            نافذة.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            نافذة.setLocationRelativeTo(null);
            نافذة.setVisible(true);
        });
    }
}
