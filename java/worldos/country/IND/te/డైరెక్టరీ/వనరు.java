// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class వనరు {
    public static void main(String[] arguments) throws Exception {
        Path దస్త్రం = Path.of("పాఠ్యము.txt");
        Files.writeString(దస్త్రం, "Hello from WorldOS!\n");
        System.out.print(Files.readString(దస్త్రం));
        SwingUtilities.invokeLater(() -> {
            JFrame విండో = new JFrame("WorldOS · OpenJDK · Swing");
            JButton బటన్ = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            బటన్.setFont(new Font("Dialog", Font.PLAIN, 24));
            బటన్.addActionListener(event -> JOptionPane.showMessageDialog(విండో, "Swing is running inside Linux."));
            విండో.add(బటన్);
            విండో.setSize(720, 200);
            విండో.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            విండో.setLocationRelativeTo(null);
            విండో.setVisible(true);
        });
    }
}
