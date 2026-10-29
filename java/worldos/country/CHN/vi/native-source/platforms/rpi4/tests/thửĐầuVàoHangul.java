// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class thửĐầuVàoHangul {
    public static void main(String[] cácĐốiSố) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame cửaSổ = new JFrame("한글 giáTrịVào · giáTrịPhôngChữ xácMinh");
            JPanel giáTrịPhiênBản = new JPanel(new BorderLayout(10, 15));
            giáTrịPhiênBản.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel HướngDẫn = new JLabel("Ctrl+Space → 한글 giáTrịVào → Ctrl+Space → Enter");
            JTextField giáTrịVào = new JTextField();
            Font giáTrịPhôngChữ = new Font("Dialog", Font.PLAIN, 20);
            HướngDẫn.setFont(giáTrịPhôngChữ.deriveFont(16f)); giáTrịVào.setFont(giáTrịPhôngChữ);
            giáTrịVào.enableInputMethods(true);
            giáTrịVào.addActionListener(sựKiện -> {
                String kếtQuả = giáTrịVào.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), kếtQuả, StandardCharsets.UTF_8);
                } catch (Exception lỗi) { throw new RuntimeException(lỗi); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(kếtQuả.getBytes(StandardCharsets.UTF_8)));
            });
            giáTrịPhiênBản.add(HướngDẫn, BorderLayout.NORTH); giáTrịPhiênBản.add(giáTrịVào, BorderLayout.CENTER);
            cửaSổ.add(giáTrịPhiênBản); cửaSổ.setSize(850, 230); cửaSổ.setLocation(100, 100);
            cửaSổ.setAlwaysOnTop(true); cửaSổ.setVisible(true); giáTrịVào.requestFocusInWindow();
            Timer chuẩnBị = new Timer(1000, sựKiện -> {
                Point vịTrí = giáTrịVào.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (vịTrí.x + 100) + " " + (vịTrí.y + 30));
            });
            chuẩnBị.setRepeats(false); chuẩnBị.start();
        });
    }
}
