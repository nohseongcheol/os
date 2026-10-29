// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class ИЗВОР {
    public static void main(String[] Аргументи) throws Exception {
        Path Датотека = Path.of("Текст.txt");
        Files.writeString(Датотека, "Hello from WorldOS!\n");
        System.out.print(Files.readString(Датотека));
        SwingUtilities.invokeLater(() -> {
            JFrame Прозор = new JFrame("WorldOS · OpenJDK · Swing");
            JButton дугме = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            дугме.setFont(new Font("Dialog", Font.PLAIN, 24));
            дугме.addActionListener(Догађај -> JOptionPane.showMessageDialog(Прозор, "Swing is running inside Linux."));
            Прозор.add(дугме);
            Прозор.setSize(720, 200);
            Прозор.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            Прозор.setLocationRelativeTo(null);
            Прозор.setVisible(true);
        });
    }
}
