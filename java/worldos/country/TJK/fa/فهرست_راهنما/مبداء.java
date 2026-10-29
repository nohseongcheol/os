// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class مبداء {
    public static void main(String[] نشانوندها) throws Exception {
        Path پرونده = Path.of("متن.txt");
        Files.writeString(پرونده, "Hello from WorldOS!\n");
        System.out.print(Files.readString(پرونده));
        SwingUtilities.invokeLater(() -> {
            JFrame window = new JFrame("WorldOS · OpenJDK · Swing");
            JButton دکمه = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            دکمه.setFont(new Font("Dialog", Font.PLAIN, 24));
            دکمه.addActionListener(event -> JOptionPane.showMessageDialog(window, "Swing is running inside Linux."));
            window.add(دکمه);
            window.setSize(720, 200);
            window.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            window.setLocationRelativeTo(null);
            window.setVisible(true);
        });
    }
}
