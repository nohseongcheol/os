// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class 한글입력시험 {
    public static void main(String[] Параметри) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame Прозорец = new JFrame("한글 입력 · шрифт_стойност проверявам");
            JPanel версия_стойност = new JPanel(new BorderLayout(10, 15));
            версия_стойност.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel 안내 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font шрифт_стойност = new Font("Dialog", Font.PLAIN, 20);
            안내.setFont(шрифт_стойност.deriveFont(16f)); 입력.setFont(шрифт_стойност);
            입력.enableInputMethods(true);
            입력.addActionListener(Събитие -> {
                String РЕЗУЛТАТ = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), РЕЗУЛТАТ, StandardCharsets.UTF_8);
                } catch (Exception ГРЕШКА) { throw new RuntimeException(ГРЕШКА); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(РЕЗУЛТАТ.getBytes(StandardCharsets.UTF_8)));
            });
            версия_стойност.add(안내, BorderLayout.NORTH); версия_стойност.add(입력, BorderLayout.CENTER);
            Прозорец.add(версия_стойност); Прозорец.setSize(850, 230); Прозорец.setLocation(100, 100);
            Прозорец.setAlwaysOnTop(true); Прозорец.setVisible(true); 입력.requestFocusInWindow();
            Timer Подготвяне = new Timer(1000, Събитие -> {
                Point Позиция = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (Позиция.x + 100) + " " + (Позиция.y + 30));
            });
            Подготвяне.setRepeats(false); Подготвяне.start();
        });
    }
}
