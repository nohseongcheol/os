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
            JFrame matapihi = new JFrame("한글 입력 · momotuhi_uara manatoko");
            JPanel putanga_uara = new JPanel(new BorderLayout(10, 15));
            putanga_uara.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel PĀNUIMAI_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font momotuhi_uara = new Font("Dialog", Font.PLAIN, 20);
            PĀNUIMAI_eb81d7d9.setFont(momotuhi_uara.deriveFont(16f)); 입력.setFont(momotuhi_uara);
            입력.enableInputMethods(true);
            입력.addActionListener(hui -> {
                String mēhua = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), mēhua, StandardCharsets.UTF_8);
                } catch (Exception Pōhēhē) { throw new RuntimeException(Pōhēhē); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(mēhua.getBytes(StandardCharsets.UTF_8)));
            });
            putanga_uara.add(PĀNUIMAI_eb81d7d9, BorderLayout.NORTH); putanga_uara.add(입력, BorderLayout.CENTER);
            matapihi.add(putanga_uara); matapihi.setSize(850, 230); matapihi.setLocation(100, 100);
            matapihi.setAlwaysOnTop(true); matapihi.setVisible(true); 입력.requestFocusInWindow();
            Timer Whakarite = new Timer(1000, hui -> {
                Point tūranga = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (tūranga.x + 100) + " " + (tūranga.y + 30));
            });
            Whakarite.setRepeats(false); Whakarite.start();
        });
    }
}
