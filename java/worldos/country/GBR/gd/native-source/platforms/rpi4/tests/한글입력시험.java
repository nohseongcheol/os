// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class 한글입력시험 {
    public static void main(String[] 인수) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame uinneag = new JFrame("한글 입력 · cruth_clò_VALUE dearbh");
            JPanel tionndadh_VALUE = new JPanel(new BorderLayout(10, 15));
            tionndadh_VALUE.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel LEUGHMI_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font cruth_clò_VALUE = new Font("Dialog", Font.PLAIN, 20);
            LEUGHMI_eb81d7d9.setFont(cruth_clò_VALUE.deriveFont(16f)); 입력.setFont(cruth_clò_VALUE);
            입력.enableInputMethods(true);
            입력.addActionListener(tachartas -> {
                String tomhas = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), tomhas, StandardCharsets.UTF_8);
                } catch (Exception Mearachd) { throw new RuntimeException(Mearachd); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(tomhas.getBytes(StandardCharsets.UTF_8)));
            });
            tionndadh_VALUE.add(LEUGHMI_eb81d7d9, BorderLayout.NORTH); tionndadh_VALUE.add(입력, BorderLayout.CENTER);
            uinneag.add(tionndadh_VALUE); uinneag.setSize(850, 230); uinneag.setLocation(100, 100);
            uinneag.setAlwaysOnTop(true); uinneag.setVisible(true); 입력.requestFocusInWindow();
            Timer Ullaich = new Timer(1000, tachartas -> {
                Point suidhich = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (suidhich.x + 100) + " " + (suidhich.y + 30));
            });
            Ullaich.setRepeats(false); Ullaich.start();
        });
    }
}
