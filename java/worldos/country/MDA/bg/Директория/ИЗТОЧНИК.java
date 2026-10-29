// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class ИЗТОЧНИК {
    public static void main(String[] Параметри) throws Exception {
        Path Файл = Path.of("Текст.txt");
        Files.writeString(Файл, "Hello from WorldOS!\n");
        System.out.print(Files.readString(Файл));
        SwingUtilities.invokeLater(() -> {
            JFrame Прозорец = new JFrame("WorldOS · OpenJDK · Swing");
            JButton бутон = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            бутон.setFont(new Font("Dialog", Font.PLAIN, 24));
            бутон.addActionListener(Събитие -> JOptionPane.showMessageDialog(Прозорец, "Swing is running inside Linux."));
            Прозорец.add(бутон);
            Прозорец.setSize(720, 200);
            Прозорец.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            Прозорец.setLocationRelativeTo(null);
            Прозорец.setVisible(true);
        });
    }
}
