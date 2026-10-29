// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class 한글입력시험 {
    public static void main(String[] Argumentu) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame Ventana = new JFrame("한글 입력 · 글꼴 확인");
            JPanel 판 = new JPanel(new BorderLayout(10, 15));
            판.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel 안내 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font 글꼴 = new Font("Dialog", Font.PLAIN, 20);
            안내.setFont(글꼴.deriveFont(16f)); 입력.setFont(글꼴);
            입력.enableInputMethods(true);
            입력.addActionListener(Eventu -> {
                String 결과 = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), 결과, StandardCharsets.UTF_8);
                } catch (Exception Fallu) { throw new RuntimeException(Fallu); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(결과.getBytes(StandardCharsets.UTF_8)));
            });
            판.add(안내, BorderLayout.NORTH); 판.add(입력, BorderLayout.CENTER);
            Ventana.add(판); Ventana.setSize(850, 230); Ventana.setLocation(100, 100);
            Ventana.setAlwaysOnTop(true); Ventana.setVisible(true); 입력.requestFocusInWindow();
            Timer 준비 = new Timer(1000, Eventu -> {
                Point Posición = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (Posición.x + 100) + " " + (Posición.y + 30));
            });
            준비.setRepeats(false); 준비.start();
        });
    }
}
