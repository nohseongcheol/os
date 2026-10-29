// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class ماخذ_فائل {
    public static void main(String[] دلائل) throws Exception {
        Path فائل_کا_نام = Path.of("متن.txt");
        Files.writeString(فائل_کا_نام, "Hello from WorldOS!\n");
        System.out.print(Files.readString(فائل_کا_نام));
        SwingUtilities.invokeLater(() -> {
            JFrame ونڈو = new JFrame("WorldOS · OpenJDK · Swing");
            JButton بٹن = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            بٹن.setFont(new Font("Dialog", Font.PLAIN, 24));
            بٹن.addActionListener(واقعہ -> JOptionPane.showMessageDialog(ونڈو, "Swing is running inside Linux."));
            ونڈو.add(بٹن);
            ونڈو.setSize(720, 200);
            ونڈو.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            ونڈو.setLocationRelativeTo(null);
            ونڈو.setVisible(true);
        });
    }
}
