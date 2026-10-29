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
            JFrame ವಿಂಡೋ = new JFrame("한글 입력 · ಫಾಂಟ್_ಮೌಲ್ಯ ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು");
            JPanel ಆವೃತ್ತಿ_ಮೌಲ್ಯ = new JPanel(new BorderLayout(10, 15));
            ಆವೃತ್ತಿ_ಮೌಲ್ಯ.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel README_ಫೈಲ್_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font ಫಾಂಟ್_ಮೌಲ್ಯ = new Font("Dialog", Font.PLAIN, 20);
            README_ಫೈಲ್_eb81d7d9.setFont(ಫಾಂಟ್_ಮೌಲ್ಯ.deriveFont(16f)); 입력.setFont(ಫಾಂಟ್_ಮೌಲ್ಯ);
            입력.enableInputMethods(true);
            입력.addActionListener(ಸಂಗತಿ -> {
                String ಮಾಪನ = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), ಮಾಪನ, StandardCharsets.UTF_8);
                } catch (Exception ದೋಷ) { throw new RuntimeException(ದೋಷ); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(ಮಾಪನ.getBytes(StandardCharsets.UTF_8)));
            });
            ಆವೃತ್ತಿ_ಮೌಲ್ಯ.add(README_ಫೈಲ್_eb81d7d9, BorderLayout.NORTH); ಆವೃತ್ತಿ_ಮೌಲ್ಯ.add(입력, BorderLayout.CENTER);
            ವಿಂಡೋ.add(ಆವೃತ್ತಿ_ಮೌಲ್ಯ); ವಿಂಡೋ.setSize(850, 230); ವಿಂಡೋ.setLocation(100, 100);
            ವಿಂಡೋ.setAlwaysOnTop(true); ವಿಂಡೋ.setVisible(true); 입력.requestFocusInWindow();
            Timer ಸಿದ್ಧಪಡಿಸು = new Timer(1000, ಸಂಗತಿ -> {
                Point ಸ್ಥಾನ = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (ಸ್ಥಾನ.x + 100) + " " + (ಸ್ಥಾನ.y + 30));
            });
            ಸಿದ್ಧಪಡಿಸು.setRepeats(false); ಸಿದ್ಧಪಡಿಸು.start();
        });
    }
}
