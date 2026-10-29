// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class 한글입력시험 {
    public static void main(String[] argumenten) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame Venster = new JFrame("한글 invoer_WAARDE · lettertype_WAARDE bevestigen");
            JPanel versie_WAARDE = new JPanel(new BorderLayout(10, 15));
            versie_WAARDE.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel LEESMIJ_eb81d7d9 = new JLabel("Ctrl+Space → 한글 invoer_WAARDE → Ctrl+Space → Enter");
            JTextField invoer_WAARDE = new JTextField();
            Font lettertype_WAARDE = new Font("Dialog", Font.PLAIN, 20);
            LEESMIJ_eb81d7d9.setFont(lettertype_WAARDE.deriveFont(16f)); invoer_WAARDE.setFont(lettertype_WAARDE);
            invoer_WAARDE.enableInputMethods(true);
            invoer_WAARDE.addActionListener(Gebeurtenis -> {
                String resultaat = invoer_WAARDE.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), resultaat, StandardCharsets.UTF_8);
                } catch (Exception fout) { throw new RuntimeException(fout); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(resultaat.getBytes(StandardCharsets.UTF_8)));
            });
            versie_WAARDE.add(LEESMIJ_eb81d7d9, BorderLayout.NORTH); versie_WAARDE.add(invoer_WAARDE, BorderLayout.CENTER);
            Venster.add(versie_WAARDE); Venster.setSize(850, 230); Venster.setLocation(100, 100);
            Venster.setAlwaysOnTop(true); Venster.setVisible(true); invoer_WAARDE.requestFocusInWindow();
            Timer Bereid_voor = new Timer(1000, Gebeurtenis -> {
                Point positie = invoer_WAARDE.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (positie.x + 100) + " " + (positie.y + 30));
            });
            Bereid_voor.setRepeats(false); Bereid_voor.start();
        });
    }
}
