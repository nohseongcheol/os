// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class ਸਰੋਤ {
    public static void main(String[] ਆਰਗੂਮੈਂਟ) throws Exception {
        Path ਫਾਇਲ = Path.of("ਟੈਕਸਟ.txt");
        Files.writeString(ਫਾਇਲ, "Hello from WorldOS!\n");
        System.out.print(Files.readString(ਫਾਇਲ));
        SwingUtilities.invokeLater(() -> {
            JFrame window = new JFrame("WorldOS · OpenJDK · Swing");
            JButton ਬਟਨ = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            ਬਟਨ.setFont(new Font("Dialog", Font.PLAIN, 24));
            ਬਟਨ.addActionListener(event -> JOptionPane.showMessageDialog(window, "Swing is running inside Linux."));
            window.add(ਬਟਨ);
            window.setSize(720, 200);
            window.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            window.setLocationRelativeTo(null);
            window.setVisible(true);
        });
    }
}
