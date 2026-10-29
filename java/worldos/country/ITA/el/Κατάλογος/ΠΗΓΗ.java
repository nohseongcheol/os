// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class ΠΗΓΗ {
    public static void main(String[] Παράμετροι) throws Exception {
        Path Αρχείο = Path.of("Κείμενο.txt");
        Files.writeString(Αρχείο, "Hello from WorldOS!\n");
        System.out.print(Files.readString(Αρχείο));
        SwingUtilities.invokeLater(() -> {
            JFrame Παράθυρο = new JFrame("WorldOS · OpenJDK · Swing");
            JButton κουμπί = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            κουμπί.setFont(new Font("Dialog", Font.PLAIN, 24));
            κουμπί.addActionListener(Συμβάν -> JOptionPane.showMessageDialog(Παράθυρο, "Swing is running inside Linux."));
            Παράθυρο.add(κουμπί);
            Παράθυρο.setSize(720, 200);
            Παράθυρο.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            Παράθυρο.setLocationRelativeTo(null);
            Παράθυρο.setVisible(true);
        });
    }
}
