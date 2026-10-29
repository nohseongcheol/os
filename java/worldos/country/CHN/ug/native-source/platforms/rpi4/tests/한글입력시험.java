// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class 한글입력시험 {
    public static void main(String[] ئۆزگەرگۈچىلەر) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame كۆزنەك = new JFrame("한글 입력 · خەت_نۇسخا_قىممىتى دەلىللىمەك");
            JPanel نەشىر_نومۇرى_قىممىتى = new JPanel(new BorderLayout(10, 15));
            نەشىر_نومۇرى_قىممىتى.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel چۈشەندۈرۈش_ھۆججىتى_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font خەت_نۇسخا_قىممىتى = new Font("Dialog", Font.PLAIN, 20);
            چۈشەندۈرۈش_ھۆججىتى_eb81d7d9.setFont(خەت_نۇسخا_قىممىتى.deriveFont(16f)); 입력.setFont(خەت_نۇسخا_قىممىتى);
            입력.enableInputMethods(true);
            입력.addActionListener(ھادىسە -> {
                String ئۆلچەم = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), ئۆلچەم, StandardCharsets.UTF_8);
                } catch (Exception خاتالىق) { throw new RuntimeException(خاتالىق); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(ئۆلچەم.getBytes(StandardCharsets.UTF_8)));
            });
            نەشىر_نومۇرى_قىممىتى.add(چۈشەندۈرۈش_ھۆججىتى_eb81d7d9, BorderLayout.NORTH); نەشىر_نومۇرى_قىممىتى.add(입력, BorderLayout.CENTER);
            كۆزنەك.add(نەشىر_نومۇرى_قىممىتى); كۆزنەك.setSize(850, 230); كۆزنەك.setLocation(100, 100);
            كۆزنەك.setAlwaysOnTop(true); كۆزنەك.setVisible(true); 입력.requestFocusInWindow();
            Timer تەييارلىماق = new Timer(1000, ھادىسە -> {
                Point ئورۇن = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (ئورۇن.x + 100) + " " + (ئورۇن.y + 30));
            });
            تەييارلىماق.setRepeats(false); تەييارلىماق.start();
        });
    }
}
