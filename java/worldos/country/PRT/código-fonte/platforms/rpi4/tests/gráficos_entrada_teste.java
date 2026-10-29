// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class gráficos_entrada_teste {
    private static boolean Chave_entrada, 누름;
    private static JFrame Janela;

    private static void verificar() {
        if (Chave_entrada && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            Janela.dispose();
            try {
                Class.forName("saudação_ae353e94").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window meta : Window.getWindows()) {
                        if (meta instanceof JFrame && meta.isVisible()
                                && ((JFrame) meta).getTitle().equals("다국어 saudação_ae353e94")) {
                            meta.toFront();
                            new Thread(() -> {
                                try {
                                    Robot sincronizar = new Robot();
                                    sincronizar.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception erro) {
                                    throw new RuntimeException(erro);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("saudação_ae353e94 창이 표시되지 않았습니다");
                });
            } catch (Exception erro) {
                throw new RuntimeException(erro);
            }
        }
    }

    public static void main(String[] argumentos) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 tela 없음");
        SwingUtilities.invokeAndWait(() -> {
            Janela = new JFrame("QEMU 키보드·마우스 testes");
            JButton botão = new JButton("한글 tela · 이 단추를 누르고 K를 entrada_VALOR");
            botão.addActionListener(Evento -> { 누름 = true; verificar(); });
            Janela.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            Janela.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent Evento) { Chave_entrada = true; verificar(); }
            });
            Janela.add(botão);
            Janela.setSize(600, 180);
            Janela.setLocation(120, 120);
            Janela.setAlwaysOnTop(true);
            Janela.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            Janela.setVisible(true);
            Janela.toFront();
            Timer Preparar = new Timer(750, Evento -> {
                Point posição = botão.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (posição.x + botão.getWidth() / 2)
                        + " " + (posição.y + botão.getHeight() / 2));
            });
            Preparar.setRepeats(false);
            Preparar.start();
        });
    }
}
