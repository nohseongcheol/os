// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class grafik_input_test {
    private static boolean tast_input, 누름;
    private static JFrame Vindue;

    private static void bekræfte() {
        if (tast_input && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            Vindue.dispose();
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
                                } catch (Exception fejl) {
                                    throw new RuntimeException(fejl);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception fejl) {
                throw new RuntimeException(fejl);
            }
        }
    }

    public static void main(String[] Argumenter) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 skærmbillede 없음");
        SwingUtilities.invokeAndWait(() -> {
            Vindue = new JFrame("QEMU 키보드·마우스 시험");
            JButton knap = new JButton("한글 skærmbillede · 이 단추를 누르고 K를 input_VÆRDI");
            knap.addActionListener(hændelse -> { 누름 = true; bekræfte(); });
            Vindue.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            Vindue.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent hændelse) { tast_input = true; bekræfte(); }
            });
            Vindue.add(knap);
            Vindue.setSize(600, 180);
            Vindue.setLocation(120, 120);
            Vindue.setAlwaysOnTop(true);
            Vindue.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            Vindue.setVisible(true);
            Vindue.toFront();
            Timer Tilrettelæg = new Timer(750, hændelse -> {
                Point Placering = knap.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (Placering.x + knap.getWidth() / 2)
                        + " " + (Placering.y + knap.getHeight() / 2));
            });
            Tilrettelæg.setRepeats(false);
            Tilrettelæg.start();
        });
    }
}
