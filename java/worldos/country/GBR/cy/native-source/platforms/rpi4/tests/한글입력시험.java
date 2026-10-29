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
            JFrame ffenestr = new JFrame("한글 입력 · ffont_VALUE dilysu");
            JPanel fersiwn_VALUE = new JPanel(new BorderLayout(10, 15));
            fersiwn_VALUE.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel GWYBODAETH_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font ffont_VALUE = new Font("Dialog", Font.PLAIN, 20);
            GWYBODAETH_eb81d7d9.setFont(ffont_VALUE.deriveFont(16f)); 입력.setFont(ffont_VALUE);
            입력.enableInputMethods(true);
            입력.addActionListener(digwyddiad -> {
                String mesur = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), mesur, StandardCharsets.UTF_8);
                } catch (Exception Gwall) { throw new RuntimeException(Gwall); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(mesur.getBytes(StandardCharsets.UTF_8)));
            });
            fersiwn_VALUE.add(GWYBODAETH_eb81d7d9, BorderLayout.NORTH); fersiwn_VALUE.add(입력, BorderLayout.CENTER);
            ffenestr.add(fersiwn_VALUE); ffenestr.setSize(850, 230); ffenestr.setLocation(100, 100);
            ffenestr.setAlwaysOnTop(true); ffenestr.setVisible(true); 입력.requestFocusInWindow();
            Timer Paratoi = new Timer(1000, digwyddiad -> {
                Point safle = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (safle.x + 100) + " " + (safle.y + 30));
            });
            Paratoi.setRepeats(false); Paratoi.start();
        });
    }
}
