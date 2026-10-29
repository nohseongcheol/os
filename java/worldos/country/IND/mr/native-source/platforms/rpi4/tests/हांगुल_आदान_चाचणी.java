// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class हांगुल_आदान_चाचणी {
    public static void main(String[] बाबी) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame विंडो = new JFrame("한글 आदान_मूल्य · फॉन्ट_मूल्य पडताळा");
            JPanel आवृत्ती_मूल्य = new JPanel(new BorderLayout(10, 15));
            आवृत्ती_मूल्य.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel वापरमार्गदर्शिका_eb81d7d9 = new JLabel("Ctrl+Space → 한글 आदान_मूल्य → Ctrl+Space → Enter");
            JTextField आदान_मूल्य = new JTextField();
            Font फॉन्ट_मूल्य = new Font("Dialog", Font.PLAIN, 20);
            वापरमार्गदर्शिका_eb81d7d9.setFont(फॉन्ट_मूल्य.deriveFont(16f)); आदान_मूल्य.setFont(फॉन्ट_मूल्य);
            आदान_मूल्य.enableInputMethods(true);
            आदान_मूल्य.addActionListener(इव्हेंट -> {
                String मोजमाप = आदान_मूल्य.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), मोजमाप, StandardCharsets.UTF_8);
                } catch (Exception त्रुटी) { throw new RuntimeException(त्रुटी); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(मोजमाप.getBytes(StandardCharsets.UTF_8)));
            });
            आवृत्ती_मूल्य.add(वापरमार्गदर्शिका_eb81d7d9, BorderLayout.NORTH); आवृत्ती_मूल्य.add(आदान_मूल्य, BorderLayout.CENTER);
            विंडो.add(आवृत्ती_मूल्य); विंडो.setSize(850, 230); विंडो.setLocation(100, 100);
            विंडो.setAlwaysOnTop(true); विंडो.setVisible(true); आदान_मूल्य.requestFocusInWindow();
            Timer तयार_करणे = new Timer(1000, इव्हेंट -> {
                Point जागा = आदान_मूल्य.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (जागा.x + 100) + " " + (जागा.y + 30));
            });
            तयार_करणे.setRepeats(false); तयार_करणे.start();
        });
    }
}
