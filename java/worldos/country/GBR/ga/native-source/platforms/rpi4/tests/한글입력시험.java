// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class 한글입력시험 {
    public static void main(String[] Argóintí) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame fuinneog = new JFrame("한글 입력 · clófhoireann_VALUE fíoraigh");
            JPanel leagan_VALUE = new JPanel(new BorderLayout(10, 15));
            leagan_VALUE.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel LÉIGHMÉ_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font clófhoireann_VALUE = new Font("Dialog", Font.PLAIN, 20);
            LÉIGHMÉ_eb81d7d9.setFont(clófhoireann_VALUE.deriveFont(16f)); 입력.setFont(clófhoireann_VALUE);
            입력.enableInputMethods(true);
            입력.addActionListener(ócáid -> {
                String tomhas = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), tomhas, StandardCharsets.UTF_8);
                } catch (Exception ERREÁID) { throw new RuntimeException(ERREÁID); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(tomhas.getBytes(StandardCharsets.UTF_8)));
            });
            leagan_VALUE.add(LÉIGHMÉ_eb81d7d9, BorderLayout.NORTH); leagan_VALUE.add(입력, BorderLayout.CENTER);
            fuinneog.add(leagan_VALUE); fuinneog.setSize(850, 230); fuinneog.setLocation(100, 100);
            fuinneog.setAlwaysOnTop(true); fuinneog.setVisible(true); 입력.requestFocusInWindow();
            Timer Ullmhaigh = new Timer(1000, ócáid -> {
                Point suíomh = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (suíomh.x + 100) + " " + (suíomh.y + 30));
            });
            Ullmhaigh.setRepeats(false); Ullmhaigh.start();
        });
    }
}
