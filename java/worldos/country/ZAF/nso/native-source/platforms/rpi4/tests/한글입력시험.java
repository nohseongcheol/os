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
            JFrame lefastere = new JFrame("한글 입력 · fonte_boleng kgonthiša");
            JPanel bešene_boleng = new JPanel(new BorderLayout(10, 15));
            bešene_boleng.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel faele_ya_MPALE_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font fonte_boleng = new Font("Dialog", Font.PLAIN, 20);
            faele_ya_MPALE_eb81d7d9.setFont(fonte_boleng.deriveFont(16f)); 입력.setFont(fonte_boleng);
            입력.enableInputMethods(true);
            입력.addActionListener(tiragalo -> {
                String 결과 = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), 결과, StandardCharsets.UTF_8);
                } catch (Exception Phošo) { throw new RuntimeException(Phošo); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(결과.getBytes(StandardCharsets.UTF_8)));
            });
            bešene_boleng.add(faele_ya_MPALE_eb81d7d9, BorderLayout.NORTH); bešene_boleng.add(입력, BorderLayout.CENTER);
            lefastere.add(bešene_boleng); lefastere.setSize(850, 230); lefastere.setLocation(100, 100);
            lefastere.setAlwaysOnTop(true); lefastere.setVisible(true); 입력.requestFocusInWindow();
            Timer Lokišetša = new Timer(1000, tiragalo -> {
                Point 위치 = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (위치.x + 100) + " " + (위치.y + 30));
            });
            Lokišetša.setRepeats(false); Lokišetša.start();
        });
    }
}
