// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class grafik_indata_test {
    private static boolean Nyckel_indata, tryck_värde;
    private static JFrame Fönster;

    private static void verifiera() {
        if (Nyckel_indata && tryck_värde) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            Fönster.dispose();
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
                                    Robot synka = new Robot();
                                    synka.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception fel) {
                                    throw new RuntimeException(fel);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception fel) {
                throw new RuntimeException(fel);
            }
        }
    }

    public static void main(String[] argument) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 skärmbild 없음");
        SwingUtilities.invokeAndWait(() -> {
            Fönster = new JFrame("QEMU 키보드·마우스 tester");
            JButton knapp = new JButton("한글 skärmbild · 이 단추를 누르고 K를 indata_värde");
            knapp.addActionListener(Händelse -> { tryck_värde = true; verifiera(); });
            Fönster.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            Fönster.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent Händelse) { Nyckel_indata = true; verifiera(); }
            });
            Fönster.add(knapp);
            Fönster.setSize(600, 180);
            Fönster.setLocation(120, 120);
            Fönster.setAlwaysOnTop(true);
            Fönster.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            Fönster.setVisible(true);
            Fönster.toFront();
            Timer Förbereda = new Timer(750, Händelse -> {
                Point position = knapp.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (position.x + knapp.getWidth() / 2)
                        + " " + (position.y + knapp.getHeight() / 2));
            });
            Förbereda.setRepeats(false);
            Förbereda.start();
        });
    }
}
