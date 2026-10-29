// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class códigoFonte {
    public static void main(String[] argumentos) throws Exception {
        Path ficheiro = Path.of("texto.txt");
        Files.writeString(ficheiro, "Hello from WorldOS!\n");
        System.out.print(Files.readString(ficheiro));
        SwingUtilities.invokeLater(() -> {
            JFrame Janela = new JFrame("WorldOS · OpenJDK · Swing");
            JButton botão = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            botão.setFont(new Font("Dialog", Font.PLAIN, 24));
            botão.addActionListener(Evento -> JOptionPane.showMessageDialog(Janela, "Swing is running inside Linux."));
            Janela.add(botão);
            Janela.setSize(720, 200);
            Janela.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            Janela.setLocationRelativeTo(null);
            Janela.setVisible(true);
        });
    }
}
