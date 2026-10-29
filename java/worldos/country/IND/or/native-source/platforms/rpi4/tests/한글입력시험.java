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
            JFrame ଓ୍ୱିଣ୍ଡୋ = new JFrame("한글 입력 · ଫଣ୍ଟ_ମୂଲ୍ୟ ଯାଞ୍ଚ୍_କରିବା");
            JPanel ସଂସ୍କରଣ_ମୂଲ୍ୟ = new JPanel(new BorderLayout(10, 15));
            ସଂସ୍କରଣ_ମୂଲ୍ୟ.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel ମତେପଢନ୍ତୁ_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font ଫଣ୍ଟ_ମୂଲ୍ୟ = new Font("Dialog", Font.PLAIN, 20);
            ମତେପଢନ୍ତୁ_eb81d7d9.setFont(ଫଣ୍ଟ_ମୂଲ୍ୟ.deriveFont(16f)); 입력.setFont(ଫଣ୍ଟ_ମୂଲ୍ୟ);
            입력.enableInputMethods(true);
            입력.addActionListener(ଘଟଣା -> {
                String ମାପ = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), ମାପ, StandardCharsets.UTF_8);
                } catch (Exception ତ୍ରୁଟି) { throw new RuntimeException(ତ୍ରୁଟି); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(ମାପ.getBytes(StandardCharsets.UTF_8)));
            });
            ସଂସ୍କରଣ_ମୂଲ୍ୟ.add(ମତେପଢନ୍ତୁ_eb81d7d9, BorderLayout.NORTH); ସଂସ୍କରଣ_ମୂଲ୍ୟ.add(입력, BorderLayout.CENTER);
            ଓ୍ୱିଣ୍ଡୋ.add(ସଂସ୍କରଣ_ମୂଲ୍ୟ); ଓ୍ୱିଣ୍ଡୋ.setSize(850, 230); ଓ୍ୱିଣ୍ଡୋ.setLocation(100, 100);
            ଓ୍ୱିଣ୍ଡୋ.setAlwaysOnTop(true); ଓ୍ୱିଣ୍ଡୋ.setVisible(true); 입력.requestFocusInWindow();
            Timer ପ୍ରସ୍ତୁତ = new Timer(1000, ଘଟଣା -> {
                Point ଅବସ୍ଥାନ = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (ଅବସ୍ଥାନ.x + 100) + " " + (ଅବସ୍ଥାନ.y + 30));
            });
            ପ୍ରସ୍ତୁତ.setRepeats(false); ପ୍ରସ୍ତୁତ.start();
        });
    }
}
