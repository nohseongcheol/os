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
            JFrame palanteer = new JFrame("한글 입력 · mbindin_xëyma luñutu");
            JPanel taalif_xëyma = new JPanel(new BorderLayout(10, 15));
            taalif_xëyma.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel JANG_MA_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font mbindin_xëyma = new Font("Dialog", Font.PLAIN, 20);
            JANG_MA_eb81d7d9.setFont(mbindin_xëyma.deriveFont(16f)); 입력.setFont(mbindin_xëyma);
            입력.enableInputMethods(true);
            입력.addActionListener(xewxew -> {
                String 결과 = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), 결과, StandardCharsets.UTF_8);
                } catch (Exception njumte) { throw new RuntimeException(njumte); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(결과.getBytes(StandardCharsets.UTF_8)));
            });
            taalif_xëyma.add(JANG_MA_eb81d7d9, BorderLayout.NORTH); taalif_xëyma.add(입력, BorderLayout.CENTER);
            palanteer.add(taalif_xëyma); palanteer.setSize(850, 230); palanteer.setLocation(100, 100);
            palanteer.setAlwaysOnTop(true); palanteer.setVisible(true); 입력.requestFocusInWindow();
            Timer jël_matuwaay = new Timer(1000, xewxew -> {
                Point 위치 = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (위치.x + 100) + " " + (위치.y + 30));
            });
            jël_matuwaay.setRepeats(false); jël_matuwaay.start();
        });
    }
}
