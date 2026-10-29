// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class __source__ {
    public static void main(String[] __arguments__) throws Exception {
        Path __file__ = Path.of("__text__.txt");
        Files.writeString(__file__, "Hello from WorldOS!\n");
        System.out.print(Files.readString(__file__));
        SwingUtilities.invokeLater(() -> {
            JFrame __window__ = new JFrame("WorldOS · OpenJDK · Swing");
            JButton __button__ = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            __button__.setFont(new Font("Dialog", Font.PLAIN, 24));
            __button__.addActionListener(__event__ -> JOptionPane.showMessageDialog(__window__, "Swing is running inside Linux."));
            __window__.add(__button__);
            __window__.setSize(720, 200);
            __window__.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            __window__.setLocationRelativeTo(null);
            __window__.setVisible(true);
        });
    }
}
