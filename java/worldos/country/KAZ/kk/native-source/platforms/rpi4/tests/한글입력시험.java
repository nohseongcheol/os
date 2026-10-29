// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class 한글입력시험 {
    public static void main(String[] Аргументтер) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame Терезе = new JFrame("한글 입력 · қаріп_мән тексеру");
            JPanel нұсқа_мән = new JPanel(new BorderLayout(10, 15));
            нұсқа_мән.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel readme_файлы_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font қаріп_мән = new Font("Dialog", Font.PLAIN, 20);
            readme_файлы_eb81d7d9.setFont(қаріп_мән.deriveFont(16f)); 입력.setFont(қаріп_мән);
            입력.enableInputMethods(true);
            입력.addActionListener(Оқиға -> {
                String НӘТИЖЕ = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), НӘТИЖЕ, StandardCharsets.UTF_8);
                } catch (Exception Қате) { throw new RuntimeException(Қате); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(НӘТИЖЕ.getBytes(StandardCharsets.UTF_8)));
            });
            нұсқа_мән.add(readme_файлы_eb81d7d9, BorderLayout.NORTH); нұсқа_мән.add(입력, BorderLayout.CENTER);
            Терезе.add(нұсқа_мән); Терезе.setSize(850, 230); Терезе.setLocation(100, 100);
            Терезе.setAlwaysOnTop(true); Терезе.setVisible(true); 입력.requestFocusInWindow();
            Timer Дайындау = new Timer(1000, Оқиға -> {
                Point Орны = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (Орны.x + 100) + " " + (Орны.y + 30));
            });
            Дайындау.setRepeats(false); Дайындау.start();
        });
    }
}
