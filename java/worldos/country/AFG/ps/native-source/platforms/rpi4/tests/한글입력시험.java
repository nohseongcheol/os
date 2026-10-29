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
            JFrame کړکۍ = new JFrame("한글 입력 · ليکبڼه_ارزښت 확인");
            JPanel 판 = new JPanel(new BorderLayout(10, 15));
            판.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel ماولوله_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font ليکبڼه_ارزښت = new Font("Dialog", Font.PLAIN, 20);
            ماولوله_eb81d7d9.setFont(ليکبڼه_ارزښت.deriveFont(16f)); 입력.setFont(ليکبڼه_ارزښت);
            입력.enableInputMethods(true);
            입력.addActionListener(پېښه -> {
                String 결과 = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), 결과, StandardCharsets.UTF_8);
                } catch (Exception تېروتنه) { throw new RuntimeException(تېروتنه); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(결과.getBytes(StandardCharsets.UTF_8)));
            });
            판.add(ماولوله_eb81d7d9, BorderLayout.NORTH); 판.add(입력, BorderLayout.CENTER);
            کړکۍ.add(판); کړکۍ.setSize(850, 230); کړکۍ.setLocation(100, 100);
            کړکۍ.setAlwaysOnTop(true); کړکۍ.setVisible(true); 입력.requestFocusInWindow();
            Timer 준비 = new Timer(1000, پېښه -> {
                Point ځای = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (ځای.x + 100) + " " + (ځای.y + 30));
            });
            준비.setRepeats(false); 준비.start();
        });
    }
}
