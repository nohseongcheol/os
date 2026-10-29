// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class FONTE {
    public static void main(String[] Argumentos) throws Exception {
        Path Ficheiro = Path.of("Texto.txt");
        Files.writeString(Ficheiro, "Hello from WorldOS!\n");
        System.out.print(Files.readString(Ficheiro));
        SwingUtilities.invokeLater(() -> {
            JFrame Xanela = new JFrame("WorldOS · OpenJDK · Swing");
            JButton botón = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            botón.setFont(new Font("Dialog", Font.PLAIN, 24));
            botón.addActionListener(Evento -> JOptionPane.showMessageDialog(Xanela, "Swing is running inside Linux."));
            Xanela.add(botón);
            Xanela.setSize(720, 200);
            Xanela.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            Xanela.setLocationRelativeTo(null);
            Xanela.setVisible(true);
        });
    }
}
