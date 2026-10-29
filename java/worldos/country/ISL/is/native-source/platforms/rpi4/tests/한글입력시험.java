// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class 한글입력시험 {
    public static void main(String[] Viðföng) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame Gluggi = new JFrame("한글 입력 · leturgerð_VALUE sannprófa");
            JPanel útgáfa_VALUE = new JPanel(new BorderLayout(10, 15));
            útgáfa_VALUE.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel LESTUMIG_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font leturgerð_VALUE = new Font("Dialog", Font.PLAIN, 20);
            LESTUMIG_eb81d7d9.setFont(leturgerð_VALUE.deriveFont(16f)); 입력.setFont(leturgerð_VALUE);
            입력.enableInputMethods(true);
            입력.addActionListener(atvik -> {
                String NIÐURSTAÐA = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), NIÐURSTAÐA, StandardCharsets.UTF_8);
                } catch (Exception Villa) { throw new RuntimeException(Villa); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(NIÐURSTAÐA.getBytes(StandardCharsets.UTF_8)));
            });
            útgáfa_VALUE.add(LESTUMIG_eb81d7d9, BorderLayout.NORTH); útgáfa_VALUE.add(입력, BorderLayout.CENTER);
            Gluggi.add(útgáfa_VALUE); Gluggi.setSize(850, 230); Gluggi.setLocation(100, 100);
            Gluggi.setAlwaysOnTop(true); Gluggi.setVisible(true); 입력.requestFocusInWindow();
            Timer Undirbúa = new Timer(1000, atvik -> {
                Point Staðsetning = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (Staðsetning.x + 100) + " " + (Staðsetning.y + 30));
            });
            Undirbúa.setRepeats(false); Undirbúa.start();
        });
    }
}
