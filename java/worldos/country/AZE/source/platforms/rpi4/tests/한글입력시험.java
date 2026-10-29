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
            JFrame pəncərə = new JFrame("한글 입력 · şrift_VALUE yoxlamaq");
            JPanel versiya_VALUE = new JPanel(new BorderLayout(10, 15));
            versiya_VALUE.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel OXUMƏNİ_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font şrift_VALUE = new Font("Dialog", Font.PLAIN, 20);
            OXUMƏNİ_eb81d7d9.setFont(şrift_VALUE.deriveFont(16f)); 입력.setFont(şrift_VALUE);
            입력.enableInputMethods(true);
            입력.addActionListener(hadisə -> {
                String ölçü = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), ölçü, StandardCharsets.UTF_8);
                } catch (Exception XƏTA) { throw new RuntimeException(XƏTA); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(ölçü.getBytes(StandardCharsets.UTF_8)));
            });
            versiya_VALUE.add(OXUMƏNİ_eb81d7d9, BorderLayout.NORTH); versiya_VALUE.add(입력, BorderLayout.CENTER);
            pəncərə.add(versiya_VALUE); pəncərə.setSize(850, 230); pəncərə.setLocation(100, 100);
            pəncərə.setAlwaysOnTop(true); pəncərə.setVisible(true); 입력.requestFocusInWindow();
            Timer Hazırla = new Timer(1000, hadisə -> {
                Point yerinə_qoymaq = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (yerinə_qoymaq.x + 100) + " " + (yerinə_qoymaq.y + 30));
            });
            Hazırla.setRepeats(false); Hazırla.start();
        });
    }
}
