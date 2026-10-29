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
            JFrame терезе = new JFrame("한글 입력 · арип_маани тууралыгын_аныктоо");
            JPanel нуска_маани = new JPanel(new BorderLayout(10, 15));
            нуска_маани.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel readme_файл_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font арип_маани = new Font("Dialog", Font.PLAIN, 20);
            readme_файл_eb81d7d9.setFont(арип_маани.deriveFont(16f)); 입력.setFont(арип_маани);
            입력.enableInputMethods(true);
            입력.addActionListener(окуя -> {
                String 결과 = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), 결과, StandardCharsets.UTF_8);
                } catch (Exception Ката) { throw new RuntimeException(Ката); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(결과.getBytes(StandardCharsets.UTF_8)));
            });
            нуска_маани.add(readme_файл_eb81d7d9, BorderLayout.NORTH); нуска_маани.add(입력, BorderLayout.CENTER);
            терезе.add(нуска_маани); терезе.setSize(850, 230); терезе.setLocation(100, 100);
            терезе.setAlwaysOnTop(true); терезе.setVisible(true); 입력.requestFocusInWindow();
            Timer Даярдоо = new Timer(1000, окуя -> {
                Point Турган_жери = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (Турган_жери.x + 100) + " " + (Турган_жери.y + 30));
            });
            Даярдоо.setRepeats(false); Даярдоо.start();
        });
    }
}
