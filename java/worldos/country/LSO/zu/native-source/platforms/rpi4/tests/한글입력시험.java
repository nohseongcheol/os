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
            JFrame ifasitela = new JFrame("한글 입력 · ubuso_bohlamvu_ifonti_inani qiniseka");
            JPanel isibuyekezo_inani = new JPanel(new BorderLayout(10, 15));
            isibuyekezo_inani.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel NGIFUNDE_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font ubuso_bohlamvu_ifonti_inani = new Font("Dialog", Font.PLAIN, 20);
            NGIFUNDE_eb81d7d9.setFont(ubuso_bohlamvu_ifonti_inani.deriveFont(16f)); 입력.setFont(ubuso_bohlamvu_ifonti_inani);
            입력.enableInputMethods(true);
            입력.addActionListener(isigameko -> {
                String 결과 = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), 결과, StandardCharsets.UTF_8);
                } catch (Exception Iphutha) { throw new RuntimeException(Iphutha); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(결과.getBytes(StandardCharsets.UTF_8)));
            });
            isibuyekezo_inani.add(NGIFUNDE_eb81d7d9, BorderLayout.NORTH); isibuyekezo_inani.add(입력, BorderLayout.CENTER);
            ifasitela.add(isibuyekezo_inani); ifasitela.setSize(850, 230); ifasitela.setLocation(100, 100);
            ifasitela.setAlwaysOnTop(true); ifasitela.setVisible(true); 입력.requestFocusInWindow();
            Timer Hlela = new Timer(1000, isigameko -> {
                Point 위치 = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (위치.x + 100) + " " + (위치.y + 30));
            });
            Hlela.setRepeats(false); Hlela.start();
        });
    }
}
