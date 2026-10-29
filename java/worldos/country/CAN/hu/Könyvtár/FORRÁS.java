// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class FORRÁS {
    public static void main(String[] Argumentumok) throws Exception {
        Path Fájl = Path.of("Szöveg.txt");
        Files.writeString(Fájl, "Hello from WorldOS!\n");
        System.out.print(Files.readString(Fájl));
        SwingUtilities.invokeLater(() -> {
            JFrame Ablak = new JFrame("WorldOS · OpenJDK · Swing");
            JButton gomb = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            gomb.setFont(new Font("Dialog", Font.PLAIN, 24));
            gomb.addActionListener(Esemény -> JOptionPane.showMessageDialog(Ablak, "Swing is running inside Linux."));
            Ablak.add(gomb);
            Ablak.setSize(720, 200);
            Ablak.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            Ablak.setLocationRelativeTo(null);
            Ablak.setVisible(true);
        });
    }
}
