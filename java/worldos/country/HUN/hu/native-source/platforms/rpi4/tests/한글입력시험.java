// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class 한글입력시험 {
    public static void main(String[] Argumentumok) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame Ablak = new JFrame("한글 bevitel_ÉRTÉK · betűkészlet_ÉRTÉK igazol");
            JPanel verzió_ÉRTÉK = new JPanel(new BorderLayout(10, 15));
            verzió_ÉRTÉK.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel fontos_fájl_eb81d7d9 = new JLabel("Ctrl+Space → 한글 bevitel_ÉRTÉK → Ctrl+Space → Enter");
            JTextField bevitel_ÉRTÉK = new JTextField();
            Font betűkészlet_ÉRTÉK = new Font("Dialog", Font.PLAIN, 20);
            fontos_fájl_eb81d7d9.setFont(betűkészlet_ÉRTÉK.deriveFont(16f)); bevitel_ÉRTÉK.setFont(betűkészlet_ÉRTÉK);
            bevitel_ÉRTÉK.enableInputMethods(true);
            bevitel_ÉRTÉK.addActionListener(Esemény -> {
                String KR = bevitel_ÉRTÉK.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), KR, StandardCharsets.UTF_8);
                } catch (Exception HIBA) { throw new RuntimeException(HIBA); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(KR.getBytes(StandardCharsets.UTF_8)));
            });
            verzió_ÉRTÉK.add(fontos_fájl_eb81d7d9, BorderLayout.NORTH); verzió_ÉRTÉK.add(bevitel_ÉRTÉK, BorderLayout.CENTER);
            Ablak.add(verzió_ÉRTÉK); Ablak.setSize(850, 230); Ablak.setLocation(100, 100);
            Ablak.setAlwaysOnTop(true); Ablak.setVisible(true); bevitel_ÉRTÉK.requestFocusInWindow();
            Timer Előkészítés = new Timer(1000, Esemény -> {
                Point Pozíció = bevitel_ÉRTÉK.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (Pozíció.x + 100) + " " + (Pozíció.y + 30));
            });
            Előkészítés.setRepeats(false); Előkészítés.start();
        });
    }
}
