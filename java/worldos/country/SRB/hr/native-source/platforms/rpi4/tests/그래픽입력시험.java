// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, pritisnuti_VALUE;
    private static JFrame Prozor;

    private static void provjeriti() {
        if (키입력 && pritisnuti_VALUE) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            Prozor.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window cilj : Window.getWindows()) {
                        if (cilj instanceof JFrame && cilj.isVisible()
                                && ((JFrame) cilj).getTitle().equals("다국어 인사")) {
                            cilj.toFront();
                            new Thread(() -> {
                                try {
                                    Robot sinkronizacija = new Robot();
                                    sinkronizacija.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception GREŠKA) {
                                    throw new RuntimeException(GREŠKA);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception GREŠKA) {
                throw new RuntimeException(GREŠKA);
            }
        }
    }

    public static void main(String[] Argumenti) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            Prozor = new JFrame("QEMU 키보드·마우스 시험");
            JButton gumb = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            gumb.addActionListener(Događaj -> { pritisnuti_VALUE = true; provjeriti(); });
            Prozor.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            Prozor.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent Događaj) { 키입력 = true; provjeriti(); }
            });
            Prozor.add(gumb);
            Prozor.setSize(600, 180);
            Prozor.setLocation(120, 120);
            Prozor.setAlwaysOnTop(true);
            Prozor.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            Prozor.setVisible(true);
            Prozor.toFront();
            Timer Pripremi = new Timer(750, Događaj -> {
                Point Položaj = gumb.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (Položaj.x + gumb.getWidth() / 2)
                        + " " + (Položaj.y + gumb.getHeight() / 2));
            });
            Pripremi.setRepeats(false);
            Pripremi.start();
        });
    }
}
