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
            JFrame መስኮት = new JFrame("한글 입력 · ቅርጸ_ቁምፊ_እሴት አረጋግጥ");
            JPanel ስሪት_እሴት = new JPanel(new BorderLayout(10, 15));
            ስሪት_እሴት.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel አንበኝ_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font ቅርጸ_ቁምፊ_እሴት = new Font("Dialog", Font.PLAIN, 20);
            አንበኝ_eb81d7d9.setFont(ቅርጸ_ቁምፊ_እሴት.deriveFont(16f)); 입력.setFont(ቅርጸ_ቁምፊ_እሴት);
            입력.enableInputMethods(true);
            입력.addActionListener(ፍጻሜ -> {
                String ልኬት = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), ልኬት, StandardCharsets.UTF_8);
                } catch (Exception ስህተት) { throw new RuntimeException(ስህተት); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(ልኬት.getBytes(StandardCharsets.UTF_8)));
            });
            ስሪት_እሴት.add(አንበኝ_eb81d7d9, BorderLayout.NORTH); ስሪት_እሴት.add(입력, BorderLayout.CENTER);
            መስኮት.add(ስሪት_እሴት); መስኮት.setSize(850, 230); መስኮት.setLocation(100, 100);
            መስኮት.setAlwaysOnTop(true); መስኮት.setVisible(true); 입력.requestFocusInWindow();
            Timer አዘጋጅ_9ce364fc = new Timer(1000, ፍጻሜ -> {
                Point አካባቢ = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (አካባቢ.x + 100) + " " + (አካባቢ.y + 30));
            });
            አዘጋጅ_9ce364fc.setRepeats(false); አዘጋጅ_9ce364fc.start();
        });
    }
}
