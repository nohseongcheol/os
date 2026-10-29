// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class 한글입력시험 {
    public static void main(String[] Argumenter) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame Vindu = new JFrame("한글 inndata_VERDI · skrift_VERDI bekrefte");
            JPanel versjon_VERDI = new JPanel(new BorderLayout(10, 15));
            versjon_VERDI.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel Viktig_fil_eb81d7d9 = new JLabel("Ctrl+Space → 한글 inndata_VERDI → Ctrl+Space → Enter");
            JTextField inndata_VERDI = new JTextField();
            Font skrift_VERDI = new Font("Dialog", Font.PLAIN, 20);
            Viktig_fil_eb81d7d9.setFont(skrift_VERDI.deriveFont(16f)); inndata_VERDI.setFont(skrift_VERDI);
            inndata_VERDI.enableInputMethods(true);
            inndata_VERDI.addActionListener(Hendelse -> {
                String KR = inndata_VERDI.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), KR, StandardCharsets.UTF_8);
                } catch (Exception feil) { throw new RuntimeException(feil); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(KR.getBytes(StandardCharsets.UTF_8)));
            });
            versjon_VERDI.add(Viktig_fil_eb81d7d9, BorderLayout.NORTH); versjon_VERDI.add(inndata_VERDI, BorderLayout.CENTER);
            Vindu.add(versjon_VERDI); Vindu.setSize(850, 230); Vindu.setLocation(100, 100);
            Vindu.setAlwaysOnTop(true); Vindu.setVisible(true); inndata_VERDI.requestFocusInWindow();
            Timer Forbered = new Timer(1000, Hendelse -> {
                Point Posisjon = inndata_VERDI.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (Posisjon.x + 100) + " " + (Posisjon.y + 30));
            });
            Forbered.setRepeats(false); Forbered.start();
        });
    }
}
