// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class fuente {
    public static void main(String[] argumentos) throws Exception {
        Path archivo = Path.of("texto.txt");
        Files.writeString(archivo, "Hello from WorldOS!\n");
        System.out.print(Files.readString(archivo));
        SwingUtilities.invokeLater(() -> {
            JFrame ventana = new JFrame("WorldOS · OpenJDK · Swing");
            JButton botón = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            botón.setFont(new Font("Dialog", Font.PLAIN, 24));
            botón.addActionListener(suceso -> JOptionPane.showMessageDialog(ventana, "Swing is running inside Linux."));
            ventana.add(botón);
            ventana.setSize(720, 200);
            ventana.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            ventana.setLocationRelativeTo(null);
            ventana.setVisible(true);
        });
    }
}
