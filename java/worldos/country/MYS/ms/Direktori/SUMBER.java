// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class SUMBER {
    public static void main(String[] arguments) throws Exception {
        Path Fail = Path.of("Teks.txt");
        Files.writeString(Fail, "Hello from WorldOS!\n");
        System.out.print(Files.readString(Fail));
        SwingUtilities.invokeLater(() -> {
            JFrame Tetingkap = new JFrame("WorldOS · OpenJDK · Swing");
            JButton Butang = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            Butang.setFont(new Font("Dialog", Font.PLAIN, 24));
            Butang.addActionListener(Peristiwa -> JOptionPane.showMessageDialog(Tetingkap, "Swing is running inside Linux."));
            Tetingkap.add(Butang);
            Tetingkap.setSize(720, 200);
            Tetingkap.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            Tetingkap.setLocationRelativeTo(null);
            Tetingkap.setVisible(true);
        });
    }
}
