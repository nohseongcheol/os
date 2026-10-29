// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class исходныйКод {
    public static void main(String[] аргументы) throws Exception {
        Path файл = Path.of("текст.txt");
        Files.writeString(файл, "Hello from WorldOS!\n");
        System.out.print(Files.readString(файл));
        SwingUtilities.invokeLater(() -> {
            JFrame Окно = new JFrame("WorldOS · OpenJDK · Swing");
            JButton кнопка = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            кнопка.setFont(new Font("Dialog", Font.PLAIN, 24));
            кнопка.addActionListener(Событие -> JOptionPane.showMessageDialog(Окно, "Swing is running inside Linux."));
            Окно.add(кнопка);
            Окно.setSize(720, 200);
            Окно.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            Окно.setLocationRelativeTo(null);
            Окно.setVisible(true);
        });
    }
}
