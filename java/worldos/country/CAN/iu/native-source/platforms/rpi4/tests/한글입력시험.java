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
            JFrame igalaangujaq = new JFrame("한글 입력 · titirausiq_atuutilik nalunairli_1aacb54c");
            JPanel imaittuuninga_atuutilik = new JPanel(new BorderLayout(10, 15));
            imaittuuninga_atuutilik.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel README_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font titirausiq_atuutilik = new Font("Dialog", Font.PLAIN, 20);
            README_eb81d7d9.setFont(titirausiq_atuutilik.deriveFont(16f)); 입력.setFont(titirausiq_atuutilik);
            입력.enableInputMethods(true);
            입력.addActionListener(piniku -> {
                String 결과 = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), 결과, StandardCharsets.UTF_8);
                } catch (Exception tammarniq) { throw new RuntimeException(tammarniq); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(결과.getBytes(StandardCharsets.UTF_8)));
            });
            imaittuuninga_atuutilik.add(README_eb81d7d9, BorderLayout.NORTH); imaittuuninga_atuutilik.add(입력, BorderLayout.CENTER);
            igalaangujaq.add(imaittuuninga_atuutilik); igalaangujaq.setSize(850, 230); igalaangujaq.setLocation(100, 100);
            igalaangujaq.setAlwaysOnTop(true); igalaangujaq.setVisible(true); 입력.requestFocusInWindow();
            Timer Parnalli = new Timer(1000, piniku -> {
                Point 위치 = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (위치.x + 100) + " " + (위치.y + 30));
            });
            Parnalli.setRepeats(false); Parnalli.start();
        });
    }
}
