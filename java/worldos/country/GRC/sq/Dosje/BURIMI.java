// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class BURIMI {
    public static void main(String[] Argumente) throws Exception {
        Path Kartelë = Path.of("Teksti.txt");
        Files.writeString(Kartelë, "Hello from WorldOS!\n");
        System.out.print(Files.readString(Kartelë));
        SwingUtilities.invokeLater(() -> {
            JFrame Dritare = new JFrame("WorldOS · OpenJDK · Swing");
            JButton Buton = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            Buton.setFont(new Font("Dialog", Font.PLAIN, 24));
            Buton.addActionListener(Ngjarje -> JOptionPane.showMessageDialog(Dritare, "Swing is running inside Linux."));
            Dritare.add(Buton);
            Dritare.setSize(720, 200);
            Dritare.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            Dritare.setLocationRelativeTo(null);
            Dritare.setVisible(true);
        });
    }
}
