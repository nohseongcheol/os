// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class 한글입력시험 {
    public static void main(String[] argument) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame Fönster = new JFrame("한글 indata_värde · teckensnitt_värde verifiera");
            JPanel version_värde = new JPanel(new BorderLayout(10, 15));
            version_värde.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel VIKTIGT_eb81d7d9 = new JLabel("Ctrl+Space → 한글 indata_värde → Ctrl+Space → Enter");
            JTextField indata_värde = new JTextField();
            Font teckensnitt_värde = new Font("Dialog", Font.PLAIN, 20);
            VIKTIGT_eb81d7d9.setFont(teckensnitt_värde.deriveFont(16f)); indata_värde.setFont(teckensnitt_värde);
            indata_värde.enableInputMethods(true);
            indata_värde.addActionListener(Händelse -> {
                String RESULTAT = indata_värde.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), RESULTAT, StandardCharsets.UTF_8);
                } catch (Exception fel) { throw new RuntimeException(fel); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(RESULTAT.getBytes(StandardCharsets.UTF_8)));
            });
            version_värde.add(VIKTIGT_eb81d7d9, BorderLayout.NORTH); version_värde.add(indata_värde, BorderLayout.CENTER);
            Fönster.add(version_värde); Fönster.setSize(850, 230); Fönster.setLocation(100, 100);
            Fönster.setAlwaysOnTop(true); Fönster.setVisible(true); indata_värde.requestFocusInWindow();
            Timer Förbereda = new Timer(1000, Händelse -> {
                Point position = indata_värde.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (position.x + 100) + " " + (position.y + 30));
            });
            Förbereda.setRepeats(false); Förbereda.start();
        });
    }
}
