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
            JFrame विंडो = new JFrame("한글 입력 · फाँट_मोल पुनर्तपासणी_करची");
            JPanel वर्जन_मोल = new JPanel(new BorderLayout(10, 15));
            वर्जन_मोल.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel README_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font फाँट_मोल = new Font("Dialog", Font.PLAIN, 20);
            README_eb81d7d9.setFont(फाँट_मोल.deriveFont(16f)); 입력.setFont(फाँट_मोल);
            입력.enableInputMethods(true);
            입력.addActionListener(प्रसंग -> {
                String मेजप = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), मेजप, StandardCharsets.UTF_8);
                } catch (Exception चूक) { throw new RuntimeException(चूक); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(मेजप.getBytes(StandardCharsets.UTF_8)));
            });
            वर्जन_मोल.add(README_eb81d7d9, BorderLayout.NORTH); वर्जन_मोल.add(입력, BorderLayout.CENTER);
            विंडो.add(वर्जन_मोल); विंडो.setSize(850, 230); विंडो.setLocation(100, 100);
            विंडो.setAlwaysOnTop(true); विंडो.setVisible(true); 입력.requestFocusInWindow();
            Timer तयार_करचें_9ce364fc = new Timer(1000, प्रसंग -> {
                Point स्थिती = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (स्थिती.x + 100) + " " + (स्थिती.y + 30));
            });
            तयार_करचें_9ce364fc.setRepeats(false); तयार_करचें_9ce364fc.start();
        });
    }
}
