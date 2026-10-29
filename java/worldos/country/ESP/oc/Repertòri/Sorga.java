// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class Sorga {
    public static void main(String[] arguments) throws Exception {
        Path Fichièr = Path.of("Tèxte.txt");
        Files.writeString(Fichièr, "Hello from WorldOS!\n");
        System.out.print(Files.readString(Fichièr));
        SwingUtilities.invokeLater(() -> {
            JFrame window = new JFrame("WorldOS · OpenJDK · Swing");
            JButton Boton = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            Boton.setFont(new Font("Dialog", Font.PLAIN, 24));
            Boton.addActionListener(Eveniment -> JOptionPane.showMessageDialog(window, "Swing is running inside Linux."));
            window.add(Boton);
            window.setSize(720, 200);
            window.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            window.setLocationRelativeTo(null);
            window.setVisible(true);
        });
    }
}
