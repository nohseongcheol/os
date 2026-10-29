// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class קודמקור {
    public static void main(String[] ארגומנטים) throws Exception {
        Path קובץ = Path.of("טקסט.txt");
        Files.writeString(קובץ, "Hello from WorldOS!\n");
        System.out.print(Files.readString(קובץ));
        SwingUtilities.invokeLater(() -> {
            JFrame חלון = new JFrame("WorldOS · OpenJDK · Swing");
            JButton לחצן = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            לחצן.setFont(new Font("Dialog", Font.PLAIN, 24));
            לחצן.addActionListener(event -> JOptionPane.showMessageDialog(חלון, "Swing is running inside Linux."));
            חלון.add(לחצן);
            חלון.setSize(720, 200);
            חלון.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            חלון.setLocationRelativeTo(null);
            חלון.setVisible(true);
        });
    }
}
