// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class Uppruni {
    public static void main(String[] Viðföng) throws Exception {
        Path Skrá = Path.of("Texti.txt");
        Files.writeString(Skrá, "Hello from WorldOS!\n");
        System.out.print(Files.readString(Skrá));
        SwingUtilities.invokeLater(() -> {
            JFrame Gluggi = new JFrame("WorldOS · OpenJDK · Swing");
            JButton hnappur = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            hnappur.setFont(new Font("Dialog", Font.PLAIN, 24));
            hnappur.addActionListener(event -> JOptionPane.showMessageDialog(Gluggi, "Swing is running inside Linux."));
            Gluggi.add(hnappur);
            Gluggi.setSize(720, 200);
            Gluggi.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            Gluggi.setLocationRelativeTo(null);
            Gluggi.setVisible(true);
        });
    }
}
