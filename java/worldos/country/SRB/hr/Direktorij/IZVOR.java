// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class IZVOR {
    public static void main(String[] Argumenti) throws Exception {
        Path Datoteka = Path.of("Tekst.txt");
        Files.writeString(Datoteka, "Hello from WorldOS!\n");
        System.out.print(Files.readString(Datoteka));
        SwingUtilities.invokeLater(() -> {
            JFrame Prozor = new JFrame("WorldOS · OpenJDK · Swing");
            JButton gumb = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            gumb.setFont(new Font("Dialog", Font.PLAIN, 24));
            gumb.addActionListener(Događaj -> JOptionPane.showMessageDialog(Prozor, "Swing is running inside Linux."));
            Prozor.add(gumb);
            Prozor.setSize(720, 200);
            Prozor.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            Prozor.setLocationRelativeTo(null);
            Prozor.setVisible(true);
        });
    }
}
