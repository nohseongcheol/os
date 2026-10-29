// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class NNONO {
    public static void main(String[] arguments) throws Exception {
        Path Fayiro = Path.of("Bigambo.txt");
        Files.writeString(Fayiro, "Hello from WorldOS!\n");
        System.out.print(Files.readString(Fayiro));
        SwingUtilities.invokeLater(() -> {
            JFrame window = new JFrame("WorldOS · OpenJDK · Swing");
            JButton ppeesa = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            ppeesa.setFont(new Font("Dialog", Font.PLAIN, 24));
            ppeesa.addActionListener(event -> JOptionPane.showMessageDialog(window, "Swing is running inside Linux."));
            window.add(ppeesa);
            window.setSize(720, 200);
            window.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            window.setLocationRelativeTo(null);
            window.setVisible(true);
        });
    }
}
