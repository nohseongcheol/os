// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class ITURBURUA {
    public static void main(String[] Argumentuak) throws Exception {
        Path Fitxategia = Path.of("Testua.txt");
        Files.writeString(Fitxategia, "Hello from WorldOS!\n");
        System.out.print(Files.readString(Fitxategia));
        SwingUtilities.invokeLater(() -> {
            JFrame Leihoa = new JFrame("WorldOS · OpenJDK · Swing");
            JButton botoia = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            botoia.setFont(new Font("Dialog", Font.PLAIN, 24));
            botoia.addActionListener(Gertaera -> JOptionPane.showMessageDialog(Leihoa, "Swing is running inside Linux."));
            Leihoa.add(botoia);
            Leihoa.setSize(720, 200);
            Leihoa.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            Leihoa.setLocationRelativeTo(null);
            Leihoa.setVisible(true);
        });
    }
}
