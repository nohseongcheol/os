// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class स्रोत {
    public static void main(String[] तर्क) throws Exception {
        Path संचिका = Path.of("पाठ.txt");
        Files.writeString(संचिका, "Hello from WorldOS!\n");
        System.out.print(Files.readString(संचिका));
        SwingUtilities.invokeLater(() -> {
            JFrame खिड़की = new JFrame("WorldOS · OpenJDK · Swing");
            JButton बटन = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            बटन.setFont(new Font("Dialog", Font.PLAIN, 24));
            बटन.addActionListener(घटना -> JOptionPane.showMessageDialog(खिड़की, "Swing is running inside Linux."));
            खिड़की.add(बटन);
            खिड़की.setSize(720, 200);
            खिड़की.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            खिड़की.setLocationRelativeTo(null);
            खिड़की.setVisible(true);
        });
    }
}
