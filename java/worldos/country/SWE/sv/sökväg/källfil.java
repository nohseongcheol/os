// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class källfil {
    public static void main(String[] argument) throws Exception {
        Path filnamn = Path.of("text.txt");
        Files.writeString(filnamn, "Hello from WorldOS!\n");
        System.out.print(Files.readString(filnamn));
        SwingUtilities.invokeLater(() -> {
            JFrame Fönster = new JFrame("WorldOS · OpenJDK · Swing");
            JButton knapp = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            knapp.setFont(new Font("Dialog", Font.PLAIN, 24));
            knapp.addActionListener(Händelse -> JOptionPane.showMessageDialog(Fönster, "Swing is running inside Linux."));
            Fönster.add(knapp);
            Fönster.setSize(720, 200);
            Fönster.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            Fönster.setLocationRelativeTo(null);
            Fönster.setVisible(true);
        });
    }
}
