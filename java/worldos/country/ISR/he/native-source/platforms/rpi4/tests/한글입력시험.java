// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class 한글입력시험 {
    public static void main(String[] ארגומנטים) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame חלון = new JFrame("한글 קלט_ערך · גופן_ערך ודא_אמת");
            JPanel גירסה_ערך = new JPanel(new BorderLayout(10, 15));
            גירסה_ערך.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel 안내 = new JLabel("Ctrl+Space → 한글 קלט_ערך → Ctrl+Space → Enter");
            JTextField קלט_ערך = new JTextField();
            Font גופן_ערך = new Font("Dialog", Font.PLAIN, 20);
            안내.setFont(גופן_ערך.deriveFont(16f)); קלט_ערך.setFont(גופן_ערך);
            קלט_ערך.enableInputMethods(true);
            קלט_ערך.addActionListener(אירוע -> {
                String תוצאה = קלט_ערך.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), תוצאה, StandardCharsets.UTF_8);
                } catch (Exception שגיאה) { throw new RuntimeException(שגיאה); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(תוצאה.getBytes(StandardCharsets.UTF_8)));
            });
            גירסה_ערך.add(안내, BorderLayout.NORTH); גירסה_ערך.add(קלט_ערך, BorderLayout.CENTER);
            חלון.add(גירסה_ערך); חלון.setSize(850, 230); חלון.setLocation(100, 100);
            חלון.setAlwaysOnTop(true); חלון.setVisible(true); קלט_ערך.requestFocusInWindow();
            Timer להכין = new Timer(1000, אירוע -> {
                Point מיקום = קלט_ערך.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (מיקום.x + 100) + " " + (מיקום.y + 30));
            });
            להכין.setRepeats(false); להכין.start();
        });
    }
}
