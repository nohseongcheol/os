// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class plik_źródłowy {
    public static void main(String[] argumenty) throws Exception {
        Path nazwa_pliku = Path.of("tekst.txt");
        Files.writeString(nazwa_pliku, "Hello from WorldOS!\n");
        System.out.print(Files.readString(nazwa_pliku));
        SwingUtilities.invokeLater(() -> {
            JFrame Okno = new JFrame("WorldOS · OpenJDK · Swing");
            JButton przycisk = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            przycisk.setFont(new Font("Dialog", Font.PLAIN, 24));
            przycisk.addActionListener(Wydarzenie -> JOptionPane.showMessageDialog(Okno, "Swing is running inside Linux."));
            Okno.add(przycisk);
            Okno.setSize(720, 200);
            Okno.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            Okno.setLocationRelativeTo(null);
            Okno.setVisible(true);
        });
    }
}
