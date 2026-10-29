// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class zdrojový_soubor {
    public static void main(String[] argumenty) throws Exception {
        Path název_souboru = Path.of("text.txt");
        Files.writeString(název_souboru, "Hello from WorldOS!\n");
        System.out.print(Files.readString(název_souboru));
        SwingUtilities.invokeLater(() -> {
            JFrame Okno = new JFrame("WorldOS · OpenJDK · Swing");
            JButton tlačítko = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            tlačítko.setFont(new Font("Dialog", Font.PLAIN, 24));
            tlačítko.addActionListener(Události -> JOptionPane.showMessageDialog(Okno, "Swing is running inside Linux."));
            Okno.add(tlačítko);
            Okno.setSize(720, 200);
            Okno.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            Okno.setLocationRelativeTo(null);
            Okno.setVisible(true);
        });
    }
}
