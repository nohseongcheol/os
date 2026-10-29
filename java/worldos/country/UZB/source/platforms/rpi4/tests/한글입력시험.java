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
            JFrame oyna = new JFrame("한글 입력 · shrift_VALUE tasdiqlamoq");
            JPanel versiya_VALUE = new JPanel(new BorderLayout(10, 15));
            versiya_VALUE.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel ma_lumot_fayli_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font shrift_VALUE = new Font("Dialog", Font.PLAIN, 20);
            ma_lumot_fayli_eb81d7d9.setFont(shrift_VALUE.deriveFont(16f)); 입력.setFont(shrift_VALUE);
            입력.enableInputMethods(true);
            입력.addActionListener(hodisa -> {
                String o_lchov = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), o_lchov, StandardCharsets.UTF_8);
                } catch (Exception Xato) { throw new RuntimeException(Xato); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(o_lchov.getBytes(StandardCharsets.UTF_8)));
            });
            versiya_VALUE.add(ma_lumot_fayli_eb81d7d9, BorderLayout.NORTH); versiya_VALUE.add(입력, BorderLayout.CENTER);
            oyna.add(versiya_VALUE); oyna.setSize(850, 230); oyna.setLocation(100, 100);
            oyna.setAlwaysOnTop(true); oyna.setVisible(true); 입력.requestFocusInWindow();
            Timer Tayyorlamoq = new Timer(1000, hodisa -> {
                Point Holati = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (Holati.x + 100) + " " + (Holati.y + 30));
            });
            Tayyorlamoq.setRepeats(false); Tayyorlamoq.start();
        });
    }
}
