// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class 한글입력시험 {
    public static void main(String[] bağımsız_değişkenler) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame Pencere = new JFrame("한글 artış_değer · yazı_tipi_değer doğrulamak");
            JPanel sürüm_değer = new JPanel(new BorderLayout(10, 15));
            sürüm_değer.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel 안내 = new JLabel("Ctrl+Space → 한글 artış_değer → Ctrl+Space → Enter");
            JTextField artış_değer = new JTextField();
            Font yazı_tipi_değer = new Font("Dialog", Font.PLAIN, 20);
            안내.setFont(yazı_tipi_değer.deriveFont(16f)); artış_değer.setFont(yazı_tipi_değer);
            artış_değer.enableInputMethods(true);
            artış_değer.addActionListener(Olay -> {
                String sonuç = artış_değer.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), sonuç, StandardCharsets.UTF_8);
                } catch (Exception hata) { throw new RuntimeException(hata); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(sonuç.getBytes(StandardCharsets.UTF_8)));
            });
            sürüm_değer.add(안내, BorderLayout.NORTH); sürüm_değer.add(artış_değer, BorderLayout.CENTER);
            Pencere.add(sürüm_değer); Pencere.setSize(850, 230); Pencere.setLocation(100, 100);
            Pencere.setAlwaysOnTop(true); Pencere.setVisible(true); artış_değer.requestFocusInWindow();
            Timer Hazırlan = new Timer(1000, Olay -> {
                Point konum = artış_değer.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (konum.x + 100) + " " + (konum.y + 30));
            });
            Hazırlan.setRepeats(false); Hazırlan.start();
        });
    }
}
