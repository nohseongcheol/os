// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class 한글입력시험 {
    public static void main(String[] អាគុយម៉ង់) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame វីនដូ = new JFrame("한글 입력 · ពុម្ពអក្សរ_តំលៃ ផ្ទៀងផ្ទាត់");
            JPanel កំណែ_តំលៃ = new JPanel(new BorderLayout(10, 15));
            កំណែ_តំលៃ.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel អានខ្ញុំ_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font ពុម្ពអក្សរ_តំលៃ = new Font("Dialog", Font.PLAIN, 20);
            អានខ្ញុំ_eb81d7d9.setFont(ពុម្ពអក្សរ_តំលៃ.deriveFont(16f)); 입력.setFont(ពុម្ពអក្សរ_តំលៃ);
            입력.enableInputMethods(true);
            입력.addActionListener(ព្រឹត្តិការណ៍ -> {
                String ការវាស់វែង = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), ការវាស់វែង, StandardCharsets.UTF_8);
                } catch (Exception កំហុស) { throw new RuntimeException(កំហុស); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(ការវាស់វែង.getBytes(StandardCharsets.UTF_8)));
            });
            កំណែ_តំលៃ.add(អានខ្ញុំ_eb81d7d9, BorderLayout.NORTH); កំណែ_តំលៃ.add(입력, BorderLayout.CENTER);
            វីនដូ.add(កំណែ_តំលៃ); វីនដូ.setSize(850, 230); វីនដូ.setLocation(100, 100);
            វីនដូ.setAlwaysOnTop(true); វីនដូ.setVisible(true); 입력.requestFocusInWindow();
            Timer រៀបចំ = new Timer(1000, ព្រឹត្តិការណ៍ -> {
                Point កំណត់ទីតាំង = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (កំណត់ទីតាំង.x + 100) + " " + (កំណត់ទីតាំង.y + 30));
            });
            រៀបចំ.setRepeats(false); រៀបចំ.start();
        });
    }
}
