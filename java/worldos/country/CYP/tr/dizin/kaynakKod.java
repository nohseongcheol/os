// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class kaynakKod {
    public static void main(String[] bağımsız_değişkenler) throws Exception {
        Path dosya = Path.of("metin.txt");
        Files.writeString(dosya, "Hello from WorldOS!\n");
        System.out.print(Files.readString(dosya));
        SwingUtilities.invokeLater(() -> {
            JFrame Pencere = new JFrame("WorldOS · OpenJDK · Swing");
            JButton düğme = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            düğme.setFont(new Font("Dialog", Font.PLAIN, 24));
            düğme.addActionListener(Olay -> JOptionPane.showMessageDialog(Pencere, "Swing is running inside Linux."));
            Pencere.add(düğme);
            Pencere.setSize(720, 200);
            Pencere.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            Pencere.setLocationRelativeTo(null);
            Pencere.setVisible(true);
        });
    }
}
