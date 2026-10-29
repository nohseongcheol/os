// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class grafica_input_test {
    private static boolean tasto_input, 누름;
    private static JFrame Finestra;

    private static void verificare() {
        if (tasto_input && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            Finestra.dispose();
            try {
                Class.forName("messaggio_di_saluto_ae353e94").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window target : Window.getWindows()) {
                        if (target instanceof JFrame && target.isVisible()
                                && ((JFrame) target).getTitle().equals("다국어 messaggio_di_saluto_ae353e94")) {
                            target.toFront();
                            new Thread(() -> {
                                try {
                                    Robot sincronizzare = new Robot();
                                    sincronizzare.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception errore) {
                                    throw new RuntimeException(errore);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("messaggio_di_saluto_ae353e94 창이 표시되지 않았습니다");
                });
            } catch (Exception errore) {
                throw new RuntimeException(errore);
            }
        }
    }

    public static void main(String[] argomenti) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 schermata 없음");
        SwingUtilities.invokeAndWait(() -> {
            Finestra = new JFrame("QEMU 키보드·마우스 prove");
            JButton pulsante = new JButton("한글 schermata · 이 단추를 누르고 K를 input_VALORE");
            pulsante.addActionListener(Evento -> { 누름 = true; verificare(); });
            Finestra.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            Finestra.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent Evento) { tasto_input = true; verificare(); }
            });
            Finestra.add(pulsante);
            Finestra.setSize(600, 180);
            Finestra.setLocation(120, 120);
            Finestra.setAlwaysOnTop(true);
            Finestra.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            Finestra.setVisible(true);
            Finestra.toFront();
            Timer Prepara = new Timer(750, Evento -> {
                Point posizione = pulsante.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (posizione.x + pulsante.getWidth() / 2)
                        + " " + (posizione.y + pulsante.getHeight() / 2));
            });
            Prepara.setRepeats(false);
            Prepara.start();
        });
    }
}
