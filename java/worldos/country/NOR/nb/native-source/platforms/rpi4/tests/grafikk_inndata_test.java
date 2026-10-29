// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class grafikk_inndata_test {
    private static boolean tast_inndata, 누름;
    private static JFrame Vindu;

    private static void bekrefte() {
        if (tast_inndata && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            Vindu.dispose();
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
                                } catch (Exception feil) {
                                    throw new RuntimeException(feil);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception feil) {
                throw new RuntimeException(feil);
            }
        }
    }

    public static void main(String[] Argumenter) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 skjermbilde 없음");
        SwingUtilities.invokeAndWait(() -> {
            Vindu = new JFrame("QEMU 키보드·마우스 시험");
            JButton Knapp = new JButton("한글 skjermbilde · 이 단추를 누르고 K를 inndata_VERDI");
            Knapp.addActionListener(Hendelse -> { 누름 = true; bekrefte(); });
            Vindu.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            Vindu.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent Hendelse) { tast_inndata = true; bekrefte(); }
            });
            Vindu.add(Knapp);
            Vindu.setSize(600, 180);
            Vindu.setLocation(120, 120);
            Vindu.setAlwaysOnTop(true);
            Vindu.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            Vindu.setVisible(true);
            Vindu.toFront();
            Timer Forbered = new Timer(750, Hendelse -> {
                Point Posisjon = Knapp.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (Posisjon.x + Knapp.getWidth() / 2)
                        + " " + (Posisjon.y + Knapp.getHeight() / 2));
            });
            Forbered.setRepeats(false);
            Forbered.start();
        });
    }
}
