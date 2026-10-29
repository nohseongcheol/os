// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class 원문 {
    public static void main(String[] 인수) throws Exception {
        Path 자료파일 = Path.of("글.txt");
        Files.writeString(자료파일, "Hello from WorldOS!\n");
        System.out.print(Files.readString(자료파일));
        SwingUtilities.invokeLater(() -> {
            JFrame 창 = new JFrame("WorldOS · OpenJDK · Swing");
            JButton 단추 = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            단추.setFont(new Font("Dialog", Font.PLAIN, 24));
            단추.addActionListener(사건 -> JOptionPane.showMessageDialog(창, "Swing is running inside Linux."));
            창.add(단추);
            창.setSize(720, 200);
            창.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            창.setLocationRelativeTo(null);
            창.setVisible(true);
        });
    }
}
