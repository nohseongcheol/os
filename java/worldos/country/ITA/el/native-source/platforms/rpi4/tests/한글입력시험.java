// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class 한글입력시험 {
    public static void main(String[] Παράμετροι) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame Παράθυρο = new JFrame("한글 είσοδος_τιμή · γραμματοσειρά_τιμή επαληθεύω");
            JPanel έκδοση_τιμή = new JPanel(new BorderLayout(10, 15));
            έκδοση_τιμή.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel αρχείο_readme_eb81d7d9 = new JLabel("Ctrl+Space → 한글 είσοδος_τιμή → Ctrl+Space → Enter");
            JTextField είσοδος_τιμή = new JTextField();
            Font γραμματοσειρά_τιμή = new Font("Dialog", Font.PLAIN, 20);
            αρχείο_readme_eb81d7d9.setFont(γραμματοσειρά_τιμή.deriveFont(16f)); είσοδος_τιμή.setFont(γραμματοσειρά_τιμή);
            είσοδος_τιμή.enableInputMethods(true);
            είσοδος_τιμή.addActionListener(Συμβάν -> {
                String μέτρηση = είσοδος_τιμή.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), μέτρηση, StandardCharsets.UTF_8);
                } catch (Exception ΣΦΑΛΜΑ) { throw new RuntimeException(ΣΦΑΛΜΑ); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(μέτρηση.getBytes(StandardCharsets.UTF_8)));
            });
            έκδοση_τιμή.add(αρχείο_readme_eb81d7d9, BorderLayout.NORTH); έκδοση_τιμή.add(είσοδος_τιμή, BorderLayout.CENTER);
            Παράθυρο.add(έκδοση_τιμή); Παράθυρο.setSize(850, 230); Παράθυρο.setLocation(100, 100);
            Παράθυρο.setAlwaysOnTop(true); Παράθυρο.setVisible(true); είσοδος_τιμή.requestFocusInWindow();
            Timer Προετοίμασε = new Timer(1000, Συμβάν -> {
                Point Θέση = είσοδος_τιμή.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (Θέση.x + 100) + " " + (Θέση.y + 30));
            });
            Προετοίμασε.setRepeats(false); Προετοίμασε.start();
        });
    }
}
