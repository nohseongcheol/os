// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class 한글입력시험 {
    public static void main(String[] argomenti) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame Finestra = new JFrame("한글 input_VALORE · tipo_di_carattere_VALORE verificare");
            JPanel versione_VALORE = new JPanel(new BorderLayout(10, 15));
            versione_VALORE.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel README_eb81d7d9 = new JLabel("Ctrl+Space → 한글 input_VALORE → Ctrl+Space → Enter");
            JTextField input_VALORE = new JTextField();
            Font tipo_di_carattere_VALORE = new Font("Dialog", Font.PLAIN, 20);
            README_eb81d7d9.setFont(tipo_di_carattere_VALORE.deriveFont(16f)); input_VALORE.setFont(tipo_di_carattere_VALORE);
            input_VALORE.enableInputMethods(true);
            input_VALORE.addActionListener(Evento -> {
                String risultato = input_VALORE.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), risultato, StandardCharsets.UTF_8);
                } catch (Exception errore) { throw new RuntimeException(errore); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(risultato.getBytes(StandardCharsets.UTF_8)));
            });
            versione_VALORE.add(README_eb81d7d9, BorderLayout.NORTH); versione_VALORE.add(input_VALORE, BorderLayout.CENTER);
            Finestra.add(versione_VALORE); Finestra.setSize(850, 230); Finestra.setLocation(100, 100);
            Finestra.setAlwaysOnTop(true); Finestra.setVisible(true); input_VALORE.requestFocusInWindow();
            Timer Prepara = new Timer(1000, Evento -> {
                Point posizione = input_VALORE.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (posizione.x + 100) + " " + (posizione.y + 30));
            });
            Prepara.setRepeats(false); Prepara.start();
        });
    }
}
