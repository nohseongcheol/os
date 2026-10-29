// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, pulsar_VALOR;
    private static JFrame Xanela;

    private static void verificar() {
        if (키입력 && pulsar_VALOR) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            Xanela.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window obxectivo_VALOR : Window.getWindows()) {
                        if (obxectivo_VALOR instanceof JFrame && obxectivo_VALOR.isVisible()
                                && ((JFrame) obxectivo_VALOR).getTitle().equals("다국어 인사")) {
                            obxectivo_VALOR.toFront();
                            new Thread(() -> {
                                try {
                                    Robot sinc = new Robot();
                                    sinc.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception ERRO) {
                                    throw new RuntimeException(ERRO);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception ERRO) {
                throw new RuntimeException(ERRO);
            }
        }
    }

    public static void main(String[] Argumentos) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            Xanela = new JFrame("QEMU 키보드·마우스 시험");
            JButton botón = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            botón.addActionListener(Evento -> { pulsar_VALOR = true; verificar(); });
            Xanela.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            Xanela.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent Evento) { 키입력 = true; verificar(); }
            });
            Xanela.add(botón);
            Xanela.setSize(600, 180);
            Xanela.setLocation(120, 120);
            Xanela.setAlwaysOnTop(true);
            Xanela.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            Xanela.setVisible(true);
            Xanela.toFront();
            Timer 준비 = new Timer(750, Evento -> {
                Point Posición = botón.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (Posición.x + botón.getWidth() / 2)
                        + " " + (Posición.y + botón.getHeight() / 2));
            });
            준비.setRepeats(false);
            준비.start();
        });
    }
}
