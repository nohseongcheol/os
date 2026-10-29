// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class ŠALTINIS {
    public static void main(String[] Argumentai) throws Exception {
        Path Failas = Path.of("Tekstas.txt");
        Files.writeString(Failas, "Hello from WorldOS!\n");
        System.out.print(Files.readString(Failas));
        SwingUtilities.invokeLater(() -> {
            JFrame Langas = new JFrame("WorldOS · OpenJDK · Swing");
            JButton mygtukas = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            mygtukas.setFont(new Font("Dialog", Font.PLAIN, 24));
            mygtukas.addActionListener(Įvykis -> JOptionPane.showMessageDialog(Langas, "Swing is running inside Linux."));
            Langas.add(mygtukas);
            Langas.setSize(720, 200);
            Langas.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            Langas.setLocationRelativeTo(null);
            Langas.setVisible(true);
        });
    }
}
