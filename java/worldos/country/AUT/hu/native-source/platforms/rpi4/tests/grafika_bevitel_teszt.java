// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class grafika_bevitel_teszt {
    private static boolean Kulcs_bevitel, 누름;
    private static JFrame Ablak;

    private static void igazol() {
        if (Kulcs_bevitel && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            Ablak.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window cél : Window.getWindows()) {
                        if (cél instanceof JFrame && cél.isVisible()
                                && ((JFrame) cél).getTitle().equals("다국어 인사")) {
                            cél.toFront();
                            new Thread(() -> {
                                try {
                                    Robot szinkronizál = new Robot();
                                    szinkronizál.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception HIBA) {
                                    throw new RuntimeException(HIBA);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception HIBA) {
                throw new RuntimeException(HIBA);
            }
        }
    }

    public static void main(String[] Argumentumok) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            Ablak = new JFrame("QEMU 키보드·마우스 시험");
            JButton gomb = new JButton("한글 화면 · 이 단추를 누르고 K를 bevitel_ÉRTÉK");
            gomb.addActionListener(Esemény -> { 누름 = true; igazol(); });
            Ablak.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            Ablak.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent Esemény) { Kulcs_bevitel = true; igazol(); }
            });
            Ablak.add(gomb);
            Ablak.setSize(600, 180);
            Ablak.setLocation(120, 120);
            Ablak.setAlwaysOnTop(true);
            Ablak.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            Ablak.setVisible(true);
            Ablak.toFront();
            Timer Előkészítés = new Timer(750, Esemény -> {
                Point Pozíció = gomb.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (Pozíció.x + gomb.getWidth() / 2)
                        + " " + (Pozíció.y + gomb.getHeight() / 2));
            });
            Előkészítés.setRepeats(false);
            Előkészítés.start();
        });
    }
}
