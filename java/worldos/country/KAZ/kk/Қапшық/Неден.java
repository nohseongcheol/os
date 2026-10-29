// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class Неден {
    public static void main(String[] Аргументтер) throws Exception {
        Path Файл = Path.of("Мәтін.txt");
        Files.writeString(Файл, "Hello from WorldOS!\n");
        System.out.print(Files.readString(Файл));
        SwingUtilities.invokeLater(() -> {
            JFrame Терезе = new JFrame("WorldOS · OpenJDK · Swing");
            JButton батырма = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            батырма.setFont(new Font("Dialog", Font.PLAIN, 24));
            батырма.addActionListener(Оқиға -> JOptionPane.showMessageDialog(Терезе, "Swing is running inside Linux."));
            Терезе.add(батырма);
            Терезе.setSize(720, 200);
            Терезе.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            Терезе.setLocationRelativeTo(null);
            Терезе.setVisible(true);
        });
    }
}
