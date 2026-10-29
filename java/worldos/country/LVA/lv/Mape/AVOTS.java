// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class AVOTS {
    public static void main(String[] Parametri) throws Exception {
        Path Fails = Path.of("Teksts.txt");
        Files.writeString(Fails, "Hello from WorldOS!\n");
        System.out.print(Files.readString(Fails));
        SwingUtilities.invokeLater(() -> {
            JFrame Logs = new JFrame("WorldOS · OpenJDK · Swing");
            JButton Pogas = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            Pogas.setFont(new Font("Dialog", Font.PLAIN, 24));
            Pogas.addActionListener(Notikums -> JOptionPane.showMessageDialog(Logs, "Swing is running inside Linux."));
            Logs.add(Pogas);
            Logs.setSize(720, 200);
            Logs.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            Logs.setLocationRelativeTo(null);
            Logs.setVisible(true);
        });
    }
}
