// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class source {
    public static void main(String[] arguments) throws Exception {
        Path Kōnae = Path.of("Ngā_kupu.txt");
        Files.writeString(Kōnae, "Hello from WorldOS!\n");
        System.out.print(Files.readString(Kōnae));
        SwingUtilities.invokeLater(() -> {
            JFrame window = new JFrame("WorldOS · OpenJDK · Swing");
            JButton button = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            button.setFont(new Font("Dialog", Font.PLAIN, 24));
            button.addActionListener(event -> JOptionPane.showMessageDialog(window, "Swing is running inside Linux."));
            window.add(button);
            window.setSize(720, 200);
            window.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            window.setLocationRelativeTo(null);
            window.setVisible(true);
        });
    }
}
