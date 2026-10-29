// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class mãNguồn {
    public static void main(String[] đối_số) throws Exception {
        Path tậpTin = Path.of("văn_bản.txt");
        Files.writeString(tậpTin, "Hello from WorldOS!\n");
        System.out.print(Files.readString(tậpTin));
        SwingUtilities.invokeLater(() -> {
            JFrame window = new JFrame("WorldOS · OpenJDK · Swing");
            JButton nút = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            nút.setFont(new Font("Dialog", Font.PLAIN, 24));
            nút.addActionListener(Sự_kiện -> JOptionPane.showMessageDialog(window, "Swing is running inside Linux."));
            window.add(nút);
            window.setSize(720, 200);
            window.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            window.setLocationRelativeTo(null);
            window.setVisible(true);
        });
    }
}
