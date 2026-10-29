// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class ALLIKAS {
    public static void main(String[] Argumendid) throws Exception {
        Path Fail = Path.of("Tekst.txt");
        Files.writeString(Fail, "Hello from WorldOS!\n");
        System.out.print(Files.readString(Fail));
        SwingUtilities.invokeLater(() -> {
            JFrame window = new JFrame("WorldOS · OpenJDK · Swing");
            JButton nupp = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            nupp.setFont(new Font("Dialog", Font.PLAIN, 24));
            nupp.addActionListener(Sündmus -> JOptionPane.showMessageDialog(window, "Swing is running inside Linux."));
            window.add(nupp);
            window.setSize(720, 200);
            window.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            window.setLocationRelativeTo(null);
            window.setVisible(true);
        });
    }
}
