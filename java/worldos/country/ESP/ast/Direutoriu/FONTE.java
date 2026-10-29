// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class FONTE {
    public static void main(String[] Argumentu) throws Exception {
        Path Ficheru = Path.of("Testu.txt");
        Files.writeString(Ficheru, "Hello from WorldOS!\n");
        System.out.print(Files.readString(Ficheru));
        SwingUtilities.invokeLater(() -> {
            JFrame Ventana = new JFrame("WorldOS · OpenJDK · Swing");
            JButton Botón = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            Botón.setFont(new Font("Dialog", Font.PLAIN, 24));
            Botón.addActionListener(Eventu -> JOptionPane.showMessageDialog(Ventana, "Swing is running inside Linux."));
            Ventana.add(Botón);
            Ventana.setSize(720, 200);
            Ventana.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            Ventana.setLocationRelativeTo(null);
            Ventana.setVisible(true);
        });
    }
}
