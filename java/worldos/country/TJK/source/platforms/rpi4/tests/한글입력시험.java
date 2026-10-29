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
            JFrame равзана = new JFrame("한글 입력 · шрифт_қимат тасдиқ_кардан");
            JPanel версия_қимат = new JPanel(new BorderLayout(10, 15));
            версия_қимат.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel файли_тафсилот_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font шрифт_қимат = new Font("Dialog", Font.PLAIN, 20);
            файли_тафсилот_eb81d7d9.setFont(шрифт_қимат.deriveFont(16f)); 입력.setFont(шрифт_қимат);
            입력.enableInputMethods(true);
            입력.addActionListener(рӯйдод -> {
                String 결과 = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), 결과, StandardCharsets.UTF_8);
                } catch (Exception Хато) { throw new RuntimeException(Хато); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(결과.getBytes(StandardCharsets.UTF_8)));
            });
            версия_қимат.add(файли_тафсилот_eb81d7d9, BorderLayout.NORTH); версия_қимат.add(입력, BorderLayout.CENTER);
            равзана.add(версия_қимат); равзана.setSize(850, 230); равзана.setLocation(100, 100);
            равзана.setAlwaysOnTop(true); равзана.setVisible(true); 입력.requestFocusInWindow();
            Timer Омода_кардан = new Timer(1000, рӯйдод -> {
                Point 위치 = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (위치.x + 100) + " " + (위치.y + 30));
            });
            Омода_кардан.setRepeats(false); Омода_кардан.start();
        });
    }
}
