// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, trykkje_VALUE;
    private static JFrame vindauge;

    private static void stadfeste() {
        if (키입력 && trykkje_VALUE) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            vindauge.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window mål : Window.getWindows()) {
                        if (mål instanceof JFrame && mål.isVisible()
                                && ((JFrame) mål).getTitle().equals("다국어 인사")) {
                            mål.toFront();
                            new Thread(() -> {
                                try {
                                    Robot synkronisere = new Robot();
                                    synkronisere.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception FEIL) {
                                    throw new RuntimeException(FEIL);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception FEIL) {
                throw new RuntimeException(FEIL);
            }
        }
    }

    public static void main(String[] Argument) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            vindauge = new JFrame("QEMU 키보드·마우스 시험");
            JButton knapp = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            knapp.addActionListener(Hending -> { trykkje_VALUE = true; stadfeste(); });
            vindauge.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            vindauge.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent Hending) { 키입력 = true; stadfeste(); }
            });
            vindauge.add(knapp);
            vindauge.setSize(600, 180);
            vindauge.setLocation(120, 120);
            vindauge.setAlwaysOnTop(true);
            vindauge.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            vindauge.setVisible(true);
            vindauge.toFront();
            Timer Klargjer = new Timer(750, Hending -> {
                Point Posisjon = knapp.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (Posisjon.x + knapp.getWidth() / 2)
                        + " " + (Posisjon.y + knapp.getHeight() / 2));
            });
            Klargjer.setRepeats(false);
            Klargjer.start();
        });
    }
}
