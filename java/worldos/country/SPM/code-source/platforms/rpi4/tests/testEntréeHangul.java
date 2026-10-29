// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class testEntréeHangul {
    public static void main(String[] arguments) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame fenêtre = new JFrame("한글 valeurEntrée · valeurPolice vérifier");
            JPanel valeurVersion = new JPanel(new BorderLayout(10, 15));
            valeurVersion.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel Guide = new JLabel("Ctrl+Space → 한글 valeurEntrée → Ctrl+Space → Enter");
            JTextField valeurEntrée = new JTextField();
            Font valeurPolice = new Font("Dialog", Font.PLAIN, 20);
            Guide.setFont(valeurPolice.deriveFont(16f)); valeurEntrée.setFont(valeurPolice);
            valeurEntrée.enableInputMethods(true);
            valeurEntrée.addActionListener(évènement -> {
                String résultat = valeurEntrée.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), résultat, StandardCharsets.UTF_8);
                } catch (Exception erreur) { throw new RuntimeException(erreur); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(résultat.getBytes(StandardCharsets.UTF_8)));
            });
            valeurVersion.add(Guide, BorderLayout.NORTH); valeurVersion.add(valeurEntrée, BorderLayout.CENTER);
            fenêtre.add(valeurVersion); fenêtre.setSize(850, 230); fenêtre.setLocation(100, 100);
            fenêtre.setAlwaysOnTop(true); fenêtre.setVisible(true); valeurEntrée.requestFocusInWindow();
            Timer préparer = new Timer(1000, évènement -> {
                Point position = valeurEntrée.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (position.x + 100) + " " + (position.y + 30));
            });
            préparer.setRepeats(false); préparer.start();
        });
    }
}
