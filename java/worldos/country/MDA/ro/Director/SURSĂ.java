// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class SURSĂ {
    public static void main(String[] Argumente) throws Exception {
        Path Fișier = Path.of("text.txt");
        Files.writeString(Fișier, "Hello from WorldOS!\n");
        System.out.print(Files.readString(Fișier));
        SwingUtilities.invokeLater(() -> {
            JFrame Fereastră = new JFrame("WorldOS · OpenJDK · Swing");
            JButton buton = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            buton.setFont(new Font("Dialog", Font.PLAIN, 24));
            buton.addActionListener(Eveniment -> JOptionPane.showMessageDialog(Fereastră, "Swing is running inside Linux."));
            Fereastră.add(buton);
            Fereastră.setSize(720, 200);
            Fereastră.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            Fereastră.setLocationRelativeTo(null);
            Fereastră.setVisible(true);
        });
    }
}
