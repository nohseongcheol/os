// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class source {
    public static void main(String[] arguments) throws Exception {
        Path fichier = Path.of("texte.txt");
        Files.writeString(fichier, "Hello from WorldOS!\n");
        System.out.print(Files.readString(fichier));
        SwingUtilities.invokeLater(() -> {
            JFrame fenêtre = new JFrame("WorldOS · OpenJDK · Swing");
            JButton bouton = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            bouton.setFont(new Font("Dialog", Font.PLAIN, 24));
            bouton.addActionListener(événement -> JOptionPane.showMessageDialog(fenêtre, "Swing is running inside Linux."));
            fenêtre.add(bouton);
            fenêtre.setSize(720, 200);
            fenêtre.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            fenêtre.setLocationRelativeTo(null);
            fenêtre.setVisible(true);
        });
    }
}
