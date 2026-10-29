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
            JFrame ფანჯარა = new JFrame("한글 입력 · შრიფტი_მნიშვნელობა გადამოწმება");
            JPanel ვერსია_მნიშვნელობა = new JPanel(new BorderLayout(10, 15));
            ვერსია_მნიშვნელობა.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel წასაკითხი_ფაილი_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font შრიფტი_მნიშვნელობა = new Font("Dialog", Font.PLAIN, 20);
            წასაკითხი_ფაილი_eb81d7d9.setFont(შრიფტი_მნიშვნელობა.deriveFont(16f)); 입력.setFont(შრიფტი_მნიშვნელობა);
            입력.enableInputMethods(true);
            입력.addActionListener(მოვლენა -> {
                String გაზომვა = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), გაზომვა, StandardCharsets.UTF_8);
                } catch (Exception შეცდომა) { throw new RuntimeException(შეცდომა); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(გაზომვა.getBytes(StandardCharsets.UTF_8)));
            });
            ვერსია_მნიშვნელობა.add(წასაკითხი_ფაილი_eb81d7d9, BorderLayout.NORTH); ვერსია_მნიშვნელობა.add(입력, BorderLayout.CENTER);
            ფანჯარა.add(ვერსია_მნიშვნელობა); ფანჯარა.setSize(850, 230); ფანჯარა.setLocation(100, 100);
            ფანჯარა.setAlwaysOnTop(true); ფანჯარა.setVisible(true); 입력.requestFocusInWindow();
            Timer მომზადება = new Timer(1000, მოვლენა -> {
                Point პოზიცია = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (პოზიცია.x + 100) + " " + (პოზიცია.y + 30));
            });
            მომზადება.setRepeats(false); მომზადება.start();
        });
    }
}
