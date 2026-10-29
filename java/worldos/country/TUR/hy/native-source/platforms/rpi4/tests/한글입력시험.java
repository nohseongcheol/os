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
            JFrame պատուհան = new JFrame("한글 입력 · տառատեսակ_արժեք հաստատել");
            JPanel տարբերակ_արժեք = new JPanel(new BorderLayout(10, 15));
            տարբերակ_արժեք.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel ԿԱՐԴԱ_ԻՆՁ_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font տառատեսակ_արժեք = new Font("Dialog", Font.PLAIN, 20);
            ԿԱՐԴԱ_ԻՆՁ_eb81d7d9.setFont(տառատեսակ_արժեք.deriveFont(16f)); 입력.setFont(տառատեսակ_արժեք);
            입력.enableInputMethods(true);
            입력.addActionListener(միջոցառում -> {
                String չափ = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), չափ, StandardCharsets.UTF_8);
                } catch (Exception Սխալ) { throw new RuntimeException(Սխալ); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(չափ.getBytes(StandardCharsets.UTF_8)));
            });
            տարբերակ_արժեք.add(ԿԱՐԴԱ_ԻՆՁ_eb81d7d9, BorderLayout.NORTH); տարբերակ_արժեք.add(입력, BorderLayout.CENTER);
            պատուհան.add(տարբերակ_արժեք); պատուհան.setSize(850, 230); պատուհան.setLocation(100, 100);
            պատուհան.setAlwaysOnTop(true); պատուհան.setVisible(true); 입력.requestFocusInWindow();
            Timer Պատրաստել = new Timer(1000, միջոցառում -> {
                Point Դիրք = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (Դիրք.x + 100) + " " + (Դիրք.y + 30));
            });
            Պատրաստել.setRepeats(false); Պատրաստել.start();
        });
    }
}
