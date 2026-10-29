// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class lähdetiedosto {
    public static void main(String[] argumentit) throws Exception {
        Path tiedoston_nimi = Path.of("teksti.txt");
        Files.writeString(tiedoston_nimi, "Hello from WorldOS!\n");
        System.out.print(Files.readString(tiedoston_nimi));
        SwingUtilities.invokeLater(() -> {
            JFrame Ikkuna = new JFrame("WorldOS · OpenJDK · Swing");
            JButton painike = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            painike.setFont(new Font("Dialog", Font.PLAIN, 24));
            painike.addActionListener(Tapahtuma -> JOptionPane.showMessageDialog(Ikkuna, "Swing is running inside Linux."));
            Ikkuna.add(painike);
            Ikkuna.setSize(720, 200);
            Ikkuna.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            Ikkuna.setLocationRelativeTo(null);
            Ikkuna.setVisible(true);
        });
    }
}
