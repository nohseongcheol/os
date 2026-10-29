// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, apăsa_VALUE;
    private static JFrame Fereastră;

    private static void verifica() {
        if (키입력 && apăsa_VALUE) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            Fereastră.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window țintă : Window.getWindows()) {
                        if (țintă instanceof JFrame && țintă.isVisible()
                                && ((JFrame) țintă).getTitle().equals("다국어 인사")) {
                            țintă.toFront();
                            new Thread(() -> {
                                try {
                                    Robot sincroniz = new Robot();
                                    sincroniz.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception eroare) {
                                    throw new RuntimeException(eroare);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception eroare) {
                throw new RuntimeException(eroare);
            }
        }
    }

    public static void main(String[] Argumente) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            Fereastră = new JFrame("QEMU 키보드·마우스 시험");
            JButton buton = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            buton.addActionListener(Eveniment -> { apăsa_VALUE = true; verifica(); });
            Fereastră.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            Fereastră.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent Eveniment) { 키입력 = true; verifica(); }
            });
            Fereastră.add(buton);
            Fereastră.setSize(600, 180);
            Fereastră.setLocation(120, 120);
            Fereastră.setAlwaysOnTop(true);
            Fereastră.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            Fereastră.setVisible(true);
            Fereastră.toFront();
            Timer Pregătiți = new Timer(750, Eveniment -> {
                Point Poziție = buton.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (Poziție.x + buton.getWidth() / 2)
                        + " " + (Poziție.y + buton.getHeight() / 2));
            });
            Pregătiți.setRepeats(false);
            Pregătiți.start();
        });
    }
}
