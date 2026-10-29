// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class codiceSorgente {
    public static void main(String[] argomenti) throws Exception {
        Path file = Path.of("testo.txt");
        Files.writeString(file, "Hello from WorldOS!\n");
        System.out.print(Files.readString(file));
        SwingUtilities.invokeLater(() -> {
            JFrame Finestra = new JFrame("WorldOS · OpenJDK · Swing");
            JButton pulsante = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            pulsante.setFont(new Font("Dialog", Font.PLAIN, 24));
            pulsante.addActionListener(Evento -> JOptionPane.showMessageDialog(Finestra, "Swing is running inside Linux."));
            Finestra.add(pulsante);
            Finestra.setSize(720, 200);
            Finestra.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            Finestra.setLocationRelativeTo(null);
            Finestra.setVisible(true);
        });
    }
}
