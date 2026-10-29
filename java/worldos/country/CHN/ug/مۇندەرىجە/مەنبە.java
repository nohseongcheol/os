// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class مەنبە {
    public static void main(String[] ئۆزگەرگۈچىلەر) throws Exception {
        Path ھۆججەت = Path.of("تېكىست.txt");
        Files.writeString(ھۆججەت, "Hello from WorldOS!\n");
        System.out.print(Files.readString(ھۆججەت));
        SwingUtilities.invokeLater(() -> {
            JFrame كۆزنەك = new JFrame("WorldOS · OpenJDK · Swing");
            JButton كۇنۇپكا = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            كۇنۇپكا.setFont(new Font("Dialog", Font.PLAIN, 24));
            كۇنۇپكا.addActionListener(ھادىسە -> JOptionPane.showMessageDialog(كۆزنەك, "Swing is running inside Linux."));
            كۆزنەك.add(كۇنۇپكا);
            كۆزنەك.setSize(720, 200);
            كۆزنەك.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            كۆزنەك.setLocationRelativeTo(null);
            كۆزنەك.setVisible(true);
        });
    }
}
