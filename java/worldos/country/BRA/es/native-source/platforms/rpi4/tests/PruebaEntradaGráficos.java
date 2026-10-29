// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class PruebaEntradaGráficos {
    private static boolean entradaTecla, valorPulsar;
    private static JFrame ventana;

    private static void verificar() {
        if (entradaTecla && valorPulsar) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            ventana.dispose();
            try {
                Class.forName("Saludo").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window valorObjetivo : Window.getWindows()) {
                        if (valorObjetivo instanceof JFrame && valorObjetivo.isVisible()
                                && ((JFrame) valorObjetivo).getTitle().equals("다국어 Saludo")) {
                            valorObjetivo.toFront();
                            new Thread(() -> {
                                try {
                                    Robot sincronizar = new Robot();
                                    sincronizar.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception error) {
                                    throw new RuntimeException(error);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("Saludo 창이 표시되지 않았습니다");
                });
            } catch (Exception error) {
                throw new RuntimeException(error);
            }
        }
    }

    public static void main(String[] argumentos) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 Pantalla métodoAusente");
        SwingUtilities.invokeAndWait(() -> {
            ventana = new JFrame("QEMU 키보드·마우스 Pruebas");
            JButton botón = new JButton("한글 Pantalla · 이 단추를 누르고 K를 valorEntrada");
            botón.addActionListener(evento -> { valorPulsar = true; verificar(); });
            ventana.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            ventana.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent evento) { entradaTecla = true; verificar(); }
            });
            ventana.add(botón);
            ventana.setSize(600, 180);
            ventana.setLocation(120, 120);
            ventana.setAlwaysOnTop(true);
            ventana.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            ventana.setVisible(true);
            ventana.toFront();
            Timer preparar = new Timer(750, evento -> {
                Point posición = botón.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (posición.x + botón.getWidth() / 2)
                        + " " + (posición.y + botón.getHeight() / 2));
            });
            preparar.setRepeats(false);
            preparar.start();
        });
    }
}
