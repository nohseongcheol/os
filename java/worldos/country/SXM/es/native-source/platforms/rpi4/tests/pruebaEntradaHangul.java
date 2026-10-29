// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class pruebaEntradaHangul {
    public static void main(String[] argumentos) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame ventana = new JFrame("한글 valorEntrada · valorFuenteTipográfica verificar");
            JPanel valorVersión = new JPanel(new BorderLayout(10, 15));
            valorVersión.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel Guía = new JLabel("Ctrl+Space → 한글 valorEntrada → Ctrl+Space → Enter");
            JTextField valorEntrada = new JTextField();
            Font valorFuenteTipográfica = new Font("Dialog", Font.PLAIN, 20);
            Guía.setFont(valorFuenteTipográfica.deriveFont(16f)); valorEntrada.setFont(valorFuenteTipográfica);
            valorEntrada.enableInputMethods(true);
            valorEntrada.addActionListener(evento -> {
                String resultado = valorEntrada.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), resultado, StandardCharsets.UTF_8);
                } catch (Exception error) { throw new RuntimeException(error); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(resultado.getBytes(StandardCharsets.UTF_8)));
            });
            valorVersión.add(Guía, BorderLayout.NORTH); valorVersión.add(valorEntrada, BorderLayout.CENTER);
            ventana.add(valorVersión); ventana.setSize(850, 230); ventana.setLocation(100, 100);
            ventana.setAlwaysOnTop(true); ventana.setVisible(true); valorEntrada.requestFocusInWindow();
            Timer preparar = new Timer(1000, evento -> {
                Point posición = valorEntrada.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (posición.x + 100) + " " + (posición.y + 30));
            });
            preparar.setRepeats(false); preparar.start();
        });
    }
}
