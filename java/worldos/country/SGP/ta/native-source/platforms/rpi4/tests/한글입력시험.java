// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class 한글입력시험 {
    public static void main(String[] செயலுருபுகள்) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame சாளரம் = new JFrame("한글 입력 · எழுத்துரு_மதிப்பு சரிபார்");
            JPanel பதிப்பு_மதிப்பு = new JPanel(new BorderLayout(10, 15));
            பதிப்பு_மதிப்பு.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel பயனர்_உதவிக்_கோப்பு_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font எழுத்துரு_மதிப்பு = new Font("Dialog", Font.PLAIN, 20);
            பயனர்_உதவிக்_கோப்பு_eb81d7d9.setFont(எழுத்துரு_மதிப்பு.deriveFont(16f)); 입력.setFont(எழுத்துரு_மதிப்பு);
            입력.enableInputMethods(true);
            입력.addActionListener(நிகழ்வு -> {
                String அளவிடக்கூடியது = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), அளவிடக்கூடியது, StandardCharsets.UTF_8);
                } catch (Exception பிழை) { throw new RuntimeException(பிழை); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(அளவிடக்கூடியது.getBytes(StandardCharsets.UTF_8)));
            });
            பதிப்பு_மதிப்பு.add(பயனர்_உதவிக்_கோப்பு_eb81d7d9, BorderLayout.NORTH); பதிப்பு_மதிப்பு.add(입력, BorderLayout.CENTER);
            சாளரம்.add(பதிப்பு_மதிப்பு); சாளரம்.setSize(850, 230); சாளரம்.setLocation(100, 100);
            சாளரம்.setAlwaysOnTop(true); சாளரம்.setVisible(true); 입력.requestFocusInWindow();
            Timer தயார்படுத்த = new Timer(1000, நிகழ்வு -> {
                Point இடம் = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (இடம்.x + 100) + " " + (இடம்.y + 30));
            });
            தயார்படுத்த.setRepeats(false); தயார்படுத்த.start();
        });
    }
}
