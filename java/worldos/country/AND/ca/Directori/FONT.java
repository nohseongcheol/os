// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class FONT {
    public static void main(String[] arguments) throws Exception {
        Path Fitxer = Path.of("text.txt");
        Files.writeString(Fitxer, "Hello from WorldOS!\n");
        System.out.print(Files.readString(Fitxer));
        SwingUtilities.invokeLater(() -> {
            JFrame Finestra = new JFrame("WorldOS · OpenJDK · Swing");
            JButton Botó = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            Botó.setFont(new Font("Dialog", Font.PLAIN, 24));
            Botó.addActionListener(Esdeveniment -> JOptionPane.showMessageDialog(Finestra, "Swing is running inside Linux."));
            Finestra.add(Botó);
            Finestra.setSize(720, 200);
            Finestra.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            Finestra.setLocationRelativeTo(null);
            Finestra.setVisible(true);
        });
    }
}
