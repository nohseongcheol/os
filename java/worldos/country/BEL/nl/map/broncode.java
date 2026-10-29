// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class broncode {
    public static void main(String[] argumenten) throws Exception {
        Path bestand = Path.of("tekst.txt");
        Files.writeString(bestand, "Hello from WorldOS!\n");
        System.out.print(Files.readString(bestand));
        SwingUtilities.invokeLater(() -> {
            JFrame Venster = new JFrame("WorldOS · OpenJDK · Swing");
            JButton knop = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            knop.setFont(new Font("Dialog", Font.PLAIN, 24));
            knop.addActionListener(Gebeurtenis -> JOptionPane.showMessageDialog(Venster, "Swing is running inside Linux."));
            Venster.add(knop);
            Venster.setSize(720, 200);
            Venster.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            Venster.setLocationRelativeTo(null);
            Venster.setVisible(true);
        });
    }
}
