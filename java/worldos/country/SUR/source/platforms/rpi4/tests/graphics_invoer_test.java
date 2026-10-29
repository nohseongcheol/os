// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class graphics_invoer_test {
    private static boolean toets_invoer, 누름;
    private static JFrame Venster;

    private static void bevestigen() {
        if (toets_invoer && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            Venster.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window doel : Window.getWindows()) {
                        if (doel instanceof JFrame && doel.isVisible()
                                && ((JFrame) doel).getTitle().equals("다국어 인사")) {
                            doel.toFront();
                            new Thread(() -> {
                                try {
                                    Robot synchroniseren = new Robot();
                                    synchroniseren.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception fout) {
                                    throw new RuntimeException(fout);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception fout) {
                throw new RuntimeException(fout);
            }
        }
    }

    public static void main(String[] argumenten) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 scherm 없음");
        SwingUtilities.invokeAndWait(() -> {
            Venster = new JFrame("QEMU 키보드·마우스 tests");
            JButton knop = new JButton("한글 scherm · 이 단추를 누르고 K를 invoer_WAARDE");
            knop.addActionListener(Gebeurtenis -> { 누름 = true; bevestigen(); });
            Venster.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            Venster.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent Gebeurtenis) { toets_invoer = true; bevestigen(); }
            });
            Venster.add(knop);
            Venster.setSize(600, 180);
            Venster.setLocation(120, 120);
            Venster.setAlwaysOnTop(true);
            Venster.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            Venster.setVisible(true);
            Venster.toFront();
            Timer Bereid_voor = new Timer(750, Gebeurtenis -> {
                Point positie = knop.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (positie.x + knop.getWidth() / 2)
                        + " " + (positie.y + knop.getHeight() / 2));
            });
            Bereid_voor.setRepeats(false);
            Bereid_voor.start();
        });
    }
}
