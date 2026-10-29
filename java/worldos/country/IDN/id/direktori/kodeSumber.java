// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class kodeSumber {
    public static void main(String[] argumen) throws Exception {
        Path berkas = Path.of("teks.txt");
        Files.writeString(berkas, "Hello from WorldOS!\n");
        System.out.print(Files.readString(berkas));
        SwingUtilities.invokeLater(() -> {
            JFrame Jendela = new JFrame("WorldOS · OpenJDK · Swing");
            JButton tombol = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            tombol.setFont(new Font("Dialog", Font.PLAIN, 24));
            tombol.addActionListener(Even -> JOptionPane.showMessageDialog(Jendela, "Swing is running inside Linux."));
            Jendela.add(tombol);
            Jendela.setSize(720, 200);
            Jendela.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            Jendela.setLocationRelativeTo(null);
            Jendela.setVisible(true);
        });
    }
}
