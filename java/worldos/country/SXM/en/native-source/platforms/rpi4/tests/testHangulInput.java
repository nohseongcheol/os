// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class testHangulInput {
    public static void main(String[] arguments) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame window = new JFrame("한글 inputValue · fontValue verify");
            JPanel versionValue = new JPanel(new BorderLayout(10, 15));
            versionValue.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel README = new JLabel("Ctrl+Space → 한글 inputValue → Ctrl+Space → Enter");
            JTextField inputValue = new JTextField();
            Font fontValue = new Font("Dialog", Font.PLAIN, 20);
            README.setFont(fontValue.deriveFont(16f)); inputValue.setFont(fontValue);
            inputValue.enableInputMethods(true);
            inputValue.addActionListener(event -> {
                String result = inputValue.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), result, StandardCharsets.UTF_8);
                } catch (Exception error) { throw new RuntimeException(error); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(result.getBytes(StandardCharsets.UTF_8)));
            });
            versionValue.add(README, BorderLayout.NORTH); versionValue.add(inputValue, BorderLayout.CENTER);
            window.add(versionValue); window.setSize(850, 230); window.setLocation(100, 100);
            window.setAlwaysOnTop(true); window.setVisible(true); inputValue.requestFocusInWindow();
            Timer prepare = new Timer(1000, event -> {
                Point position = inputValue.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (position.x + 100) + " " + (position.y + 30));
            });
            prepare.setRepeats(false); prepare.start();
        });
    }
}
