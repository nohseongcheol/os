// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class ZDROJ {
    public static void main(String[] Argumenty) throws Exception {
        Path Súbor = Path.of("Spracovanie_textu.txt");
        Files.writeString(Súbor, "Hello from WorldOS!\n");
        System.out.print(Files.readString(Súbor));
        SwingUtilities.invokeLater(() -> {
            JFrame Okno = new JFrame("WorldOS · OpenJDK · Swing");
            JButton Tlačidlo = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            Tlačidlo.setFont(new Font("Dialog", Font.PLAIN, 24));
            Tlačidlo.addActionListener(Udalosť -> JOptionPane.showMessageDialog(Okno, "Swing is running inside Linux."));
            Okno.add(Tlačidlo);
            Okno.setSize(720, 200);
            Okno.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            Okno.setLocationRelativeTo(null);
            Okno.setVisible(true);
        });
    }
}
