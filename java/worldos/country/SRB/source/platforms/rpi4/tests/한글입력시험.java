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
            JFrame Прозор = new JFrame("한글 입력 · фонт_вриједност потврдити");
            JPanel верзија_вриједност = new JPanel(new BorderLayout(10, 15));
            верзија_вриједност.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel Прочитај_ме_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font фонт_вриједност = new Font("Dialog", Font.PLAIN, 20);
            Прочитај_ме_eb81d7d9.setFont(фонт_вриједност.deriveFont(16f)); 입력.setFont(фонт_вриједност);
            입력.enableInputMethods(true);
            입력.addActionListener(Догађај -> {
                String ИСХОД = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), ИСХОД, StandardCharsets.UTF_8);
                } catch (Exception ГРЕШКА) { throw new RuntimeException(ГРЕШКА); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(ИСХОД.getBytes(StandardCharsets.UTF_8)));
            });
            верзија_вриједност.add(Прочитај_ме_eb81d7d9, BorderLayout.NORTH); верзија_вриједност.add(입력, BorderLayout.CENTER);
            Прозор.add(верзија_вриједност); Прозор.setSize(850, 230); Прозор.setLocation(100, 100);
            Прозор.setAlwaysOnTop(true); Прозор.setVisible(true); 입력.requestFocusInWindow();
            Timer Припремити = new Timer(1000, Догађај -> {
                Point Положај = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (Положај.x + 100) + " " + (Положај.y + 30));
            });
            Припремити.setRepeats(false); Припремити.start();
        });
    }
}
