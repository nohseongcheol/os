// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class Quelltext {
    public static void main(String[] Argumente) throws Exception {
        Path Datei = Path.of("Text.txt");
        Files.writeString(Datei, "Hello from WorldOS!\n");
        System.out.print(Files.readString(Datei));
        SwingUtilities.invokeLater(() -> {
            JFrame Fenster = new JFrame("WorldOS · OpenJDK · Swing");
            JButton Schaltfläche = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            Schaltfläche.setFont(new Font("Dialog", Font.PLAIN, 24));
            Schaltfläche.addActionListener(Ereignis -> JOptionPane.showMessageDialog(Fenster, "Swing is running inside Linux."));
            Fenster.add(Schaltfläche);
            Fenster.setSize(720, 200);
            Fenster.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            Fenster.setLocationRelativeTo(null);
            Fenster.setVisible(true);
        });
    }
}
