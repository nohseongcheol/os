// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class VIR {
    public static void main(String[] Argumenti) throws Exception {
        Path Datoteka = Path.of("Besedilo.txt");
        Files.writeString(Datoteka, "Hello from WorldOS!\n");
        System.out.print(Files.readString(Datoteka));
        SwingUtilities.invokeLater(() -> {
            JFrame window = new JFrame("WorldOS · OpenJDK · Swing");
            JButton Gumb = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            Gumb.setFont(new Font("Dialog", Font.PLAIN, 24));
            Gumb.addActionListener(event -> JOptionPane.showMessageDialog(window, "Swing is running inside Linux."));
            window.add(Gumb);
            window.setSize(720, 200);
            window.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            window.setLocationRelativeTo(null);
            window.setVisible(true);
        });
    }
}
