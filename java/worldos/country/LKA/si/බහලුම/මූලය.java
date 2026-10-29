// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class මූලය {
    public static void main(String[] විස්තාරක) throws Exception {
        Path ගොනු = Path.of("පෙළ.txt");
        Files.writeString(ගොනු, "Hello from WorldOS!\n");
        System.out.print(Files.readString(ගොනු));
        SwingUtilities.invokeLater(() -> {
            JFrame කවුළුව = new JFrame("WorldOS · OpenJDK · Swing");
            JButton button = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            button.setFont(new Font("Dialog", Font.PLAIN, 24));
            button.addActionListener(සිදුවීම -> JOptionPane.showMessageDialog(කවුළුව, "Swing is running inside Linux."));
            කවුළුව.add(button);
            කවුළුව.setSize(720, 200);
            කවුළුව.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            කවුළුව.setLocationRelativeTo(null);
            කවුළුව.setVisible(true);
        });
    }
}
