// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class 한글입력시험 {
    public static void main(String[] ਆਰਗੂਮੈਂਟ) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame ਵਿੰਡੋ = new JFrame("한글 입력 · ਫੌਂਟ_ਕੀਮਤ ਤਸਦੀਕ");
            JPanel ਵਰਜ਼ਨ_ਕੀਮਤ = new JPanel(new BorderLayout(10, 15));
            ਵਰਜ਼ਨ_ਕੀਮਤ.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel ਫਈਲ_ਮੈਨੂੰ_ਪੜਨ_ਦਿਉ_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font ਫੌਂਟ_ਕੀਮਤ = new Font("Dialog", Font.PLAIN, 20);
            ਫਈਲ_ਮੈਨੂੰ_ਪੜਨ_ਦਿਉ_eb81d7d9.setFont(ਫੌਂਟ_ਕੀਮਤ.deriveFont(16f)); 입력.setFont(ਫੌਂਟ_ਕੀਮਤ);
            입력.enableInputMethods(true);
            입력.addActionListener(ਇਵੈਂਟ -> {
                String ਮਾਪ = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), ਮਾਪ, StandardCharsets.UTF_8);
                } catch (Exception ਗਲਤੀ) { throw new RuntimeException(ਗਲਤੀ); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(ਮਾਪ.getBytes(StandardCharsets.UTF_8)));
            });
            ਵਰਜ਼ਨ_ਕੀਮਤ.add(ਫਈਲ_ਮੈਨੂੰ_ਪੜਨ_ਦਿਉ_eb81d7d9, BorderLayout.NORTH); ਵਰਜ਼ਨ_ਕੀਮਤ.add(입력, BorderLayout.CENTER);
            ਵਿੰਡੋ.add(ਵਰਜ਼ਨ_ਕੀਮਤ); ਵਿੰਡੋ.setSize(850, 230); ਵਿੰਡੋ.setLocation(100, 100);
            ਵਿੰਡੋ.setAlwaysOnTop(true); ਵਿੰਡੋ.setVisible(true); 입력.requestFocusInWindow();
            Timer ਤਿਆਰ_ਕਰੋ = new Timer(1000, ਇਵੈਂਟ -> {
                Point ਸਥਿਤੀ = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (ਸਥਿਤੀ.x + 100) + " " + (ਸਥਿਤੀ.y + 30));
            });
            ਤਿਆਰ_ਕਰੋ.setRepeats(false); ਤਿਆਰ_ਕਰੋ.start();
        });
    }
}
