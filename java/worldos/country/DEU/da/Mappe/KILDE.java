// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class KILDE {
    public static void main(String[] Argumenter) throws Exception {
        Path Fil = Path.of("Tekst.txt");
        Files.writeString(Fil, "Hello from WorldOS!\n");
        System.out.print(Files.readString(Fil));
        SwingUtilities.invokeLater(() -> {
            JFrame Vindue = new JFrame("WorldOS · OpenJDK · Swing");
            JButton knap = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            knap.setFont(new Font("Dialog", Font.PLAIN, 24));
            knap.addActionListener(event -> JOptionPane.showMessageDialog(Vindue, "Swing is running inside Linux."));
            Vindue.add(knap);
            Vindue.setSize(720, 200);
            Vindue.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            Vindue.setLocationRelativeTo(null);
            Vindue.setVisible(true);
        });
    }
}
