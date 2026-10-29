// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class 한글입력시험 {
    public static void main(String[] Argumenter) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame Vindue = new JFrame("한글 input_VÆRDI · skrifttype_VÆRDI bekræfte");
            JPanel version_VÆRDI = new JPanel(new BorderLayout(10, 15));
            version_VÆRDI.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel Vigtigt_eb81d7d9 = new JLabel("Ctrl+Space → 한글 input_VÆRDI → Ctrl+Space → Enter");
            JTextField input_VÆRDI = new JTextField();
            Font skrifttype_VÆRDI = new Font("Dialog", Font.PLAIN, 20);
            Vigtigt_eb81d7d9.setFont(skrifttype_VÆRDI.deriveFont(16f)); input_VÆRDI.setFont(skrifttype_VÆRDI);
            input_VÆRDI.enableInputMethods(true);
            input_VÆRDI.addActionListener(hændelse -> {
                String KR = input_VÆRDI.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), KR, StandardCharsets.UTF_8);
                } catch (Exception fejl) { throw new RuntimeException(fejl); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(KR.getBytes(StandardCharsets.UTF_8)));
            });
            version_VÆRDI.add(Vigtigt_eb81d7d9, BorderLayout.NORTH); version_VÆRDI.add(input_VÆRDI, BorderLayout.CENTER);
            Vindue.add(version_VÆRDI); Vindue.setSize(850, 230); Vindue.setLocation(100, 100);
            Vindue.setAlwaysOnTop(true); Vindue.setVisible(true); input_VÆRDI.requestFocusInWindow();
            Timer Tilrettelæg = new Timer(1000, hændelse -> {
                Point Placering = input_VÆRDI.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (Placering.x + 100) + " " + (Placering.y + 30));
            });
            Tilrettelæg.setRepeats(false); Tilrettelæg.start();
        });
    }
}
