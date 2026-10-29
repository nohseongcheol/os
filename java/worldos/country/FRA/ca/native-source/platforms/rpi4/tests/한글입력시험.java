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
            JFrame Finestra = new JFrame("한글 입력 · tipus_de_lletra_VALOR verificar");
            JPanel versió_VALOR = new JPanel(new BorderLayout(10, 15));
            versió_VALOR.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel LLEGIU_ME_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font tipus_de_lletra_VALOR = new Font("Dialog", Font.PLAIN, 20);
            LLEGIU_ME_eb81d7d9.setFont(tipus_de_lletra_VALOR.deriveFont(16f)); 입력.setFont(tipus_de_lletra_VALOR);
            입력.enableInputMethods(true);
            입력.addActionListener(Esdeveniment -> {
                String RESULTAT = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), RESULTAT, StandardCharsets.UTF_8);
                } catch (Exception s_ha_produït_un_error) { throw new RuntimeException(s_ha_produït_un_error); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(RESULTAT.getBytes(StandardCharsets.UTF_8)));
            });
            versió_VALOR.add(LLEGIU_ME_eb81d7d9, BorderLayout.NORTH); versió_VALOR.add(입력, BorderLayout.CENTER);
            Finestra.add(versió_VALOR); Finestra.setSize(850, 230); Finestra.setLocation(100, 100);
            Finestra.setAlwaysOnTop(true); Finestra.setVisible(true); 입력.requestFocusInWindow();
            Timer Prepara = new Timer(1000, Esdeveniment -> {
                Point Posició = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (Posició.x + 100) + " " + (Posició.y + 30));
            });
            Prepara.setRepeats(false); Prepara.start();
        });
    }
}
