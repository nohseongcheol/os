// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class 한글입력시험 {
    public static void main(String[] Argumentos) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame Xanela = new JFrame("한글 입력 · tipo_de_letra_VALOR verificar");
            JPanel versión_VALOR = new JPanel(new BorderLayout(10, 15));
            versión_VALOR.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel Léame_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font tipo_de_letra_VALOR = new Font("Dialog", Font.PLAIN, 20);
            Léame_eb81d7d9.setFont(tipo_de_letra_VALOR.deriveFont(16f)); 입력.setFont(tipo_de_letra_VALOR);
            입력.enableInputMethods(true);
            입력.addActionListener(Evento -> {
                String RESULTANTE = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), RESULTANTE, StandardCharsets.UTF_8);
                } catch (Exception ERRO) { throw new RuntimeException(ERRO); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(RESULTANTE.getBytes(StandardCharsets.UTF_8)));
            });
            versión_VALOR.add(Léame_eb81d7d9, BorderLayout.NORTH); versión_VALOR.add(입력, BorderLayout.CENTER);
            Xanela.add(versión_VALOR); Xanela.setSize(850, 230); Xanela.setLocation(100, 100);
            Xanela.setAlwaysOnTop(true); Xanela.setVisible(true); 입력.requestFocusInWindow();
            Timer 준비 = new Timer(1000, Evento -> {
                Point Posición = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (Posición.x + 100) + " " + (Posición.y + 30));
            });
            준비.setRepeats(false); 준비.start();
        });
    }
}
