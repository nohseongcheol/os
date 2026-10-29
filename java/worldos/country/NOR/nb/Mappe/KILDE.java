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
            JFrame Vindu = new JFrame("WorldOS · OpenJDK · Swing");
            JButton Knapp = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            Knapp.setFont(new Font("Dialog", Font.PLAIN, 24));
            Knapp.addActionListener(Hendelse -> JOptionPane.showMessageDialog(Vindu, "Swing is running inside Linux."));
            Vindu.add(Knapp);
            Vindu.setSize(720, 200);
            Vindu.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            Vindu.setLocationRelativeTo(null);
            Vindu.setVisible(true);
        });
    }
}
