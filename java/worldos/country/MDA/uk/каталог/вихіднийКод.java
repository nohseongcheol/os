// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class вихіднийКод {
    public static void main(String[] аргументи) throws Exception {
        Path файл = Path.of("текст.txt");
        Files.writeString(файл, "Hello from WorldOS!\n");
        System.out.print(Files.readString(файл));
        SwingUtilities.invokeLater(() -> {
            JFrame Вікно = new JFrame("WorldOS · OpenJDK · Swing");
            JButton кнопка = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            кнопка.setFont(new Font("Dialog", Font.PLAIN, 24));
            кнопка.addActionListener(Подія -> JOptionPane.showMessageDialog(Вікно, "Swing is running inside Linux."));
            Вікно.add(кнопка);
            Вікно.setSize(720, 200);
            Вікно.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            Вікно.setLocationRelativeTo(null);
            Вікно.setVisible(true);
        });
    }
}
