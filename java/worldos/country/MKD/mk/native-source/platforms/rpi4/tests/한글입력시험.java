// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class 한글입력시험 {
    public static void main(String[] Аргументи) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame прозорец = new JFrame("한글 입력 · фонт_VALUE провери");
            JPanel верзија_VALUE = new JPanel(new BorderLayout(10, 15));
            верзија_VALUE.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel информации_пред_употреба_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font фонт_VALUE = new Font("Dialog", Font.PLAIN, 20);
            информации_пред_употреба_eb81d7d9.setFont(фонт_VALUE.deriveFont(16f)); 입력.setFont(фонт_VALUE);
            입력.enableInputMethods(true);
            입력.addActionListener(настан -> {
                String мерка = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), мерка, StandardCharsets.UTF_8);
                } catch (Exception ГРЕШКА) { throw new RuntimeException(ГРЕШКА); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(мерка.getBytes(StandardCharsets.UTF_8)));
            });
            верзија_VALUE.add(информации_пред_употреба_eb81d7d9, BorderLayout.NORTH); верзија_VALUE.add(입력, BorderLayout.CENTER);
            прозорец.add(верзија_VALUE); прозорец.setSize(850, 230); прозорец.setLocation(100, 100);
            прозорец.setAlwaysOnTop(true); прозорец.setVisible(true); 입력.requestFocusInWindow();
            Timer Подготви = new Timer(1000, настан -> {
                Point Позиција = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (Позиција.x + 100) + " " + (Позиција.y + 30));
            });
            Подготви.setRepeats(false); Подготви.start();
        });
    }
}
