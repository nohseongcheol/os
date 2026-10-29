// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class 한글입력시험 {
    public static void main(String[] argumentos) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame Janela = new JFrame("한글 entrada_VALOR · fonte_VALOR verificar");
            JPanel versão_VALOR = new JPanel(new BorderLayout(10, 15));
            versão_VALOR.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel LEIAME_eb81d7d9 = new JLabel("Ctrl+Space → 한글 entrada_VALOR → Ctrl+Space → Enter");
            JTextField entrada_VALOR = new JTextField();
            Font fonte_VALOR = new Font("Dialog", Font.PLAIN, 20);
            LEIAME_eb81d7d9.setFont(fonte_VALOR.deriveFont(16f)); entrada_VALOR.setFont(fonte_VALOR);
            entrada_VALOR.enableInputMethods(true);
            entrada_VALOR.addActionListener(Evento -> {
                String resultado = entrada_VALOR.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), resultado, StandardCharsets.UTF_8);
                } catch (Exception erro) { throw new RuntimeException(erro); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(resultado.getBytes(StandardCharsets.UTF_8)));
            });
            versão_VALOR.add(LEIAME_eb81d7d9, BorderLayout.NORTH); versão_VALOR.add(entrada_VALOR, BorderLayout.CENTER);
            Janela.add(versão_VALOR); Janela.setSize(850, 230); Janela.setLocation(100, 100);
            Janela.setAlwaysOnTop(true); Janela.setVisible(true); entrada_VALOR.requestFocusInWindow();
            Timer Preparar = new Timer(1000, Evento -> {
                Point posição = entrada_VALOR.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (posição.x + 100) + " " + (posição.y + 30));
            });
            Preparar.setRepeats(false); Preparar.start();
        });
    }
}
