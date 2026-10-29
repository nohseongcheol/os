// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, pritisniti_VALUE;
    private static JFrame okno;

    private static void 확인() {
        if (키입력 && pritisniti_VALUE) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            okno.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window tarča : Window.getWindows()) {
                        if (tarča instanceof JFrame && tarča.isVisible()
                                && ((JFrame) tarča).getTitle().equals("다국어 인사")) {
                            tarča.toFront();
                            new Thread(() -> {
                                try {
                                    Robot sinhronizirati = new Robot();
                                    sinhronizirati.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception NAPAKA) {
                                    throw new RuntimeException(NAPAKA);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception NAPAKA) {
                throw new RuntimeException(NAPAKA);
            }
        }
    }

    public static void main(String[] Argumenti) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            okno = new JFrame("QEMU 키보드·마우스 시험");
            JButton Gumb = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            Gumb.addActionListener(dogodek -> { pritisniti_VALUE = true; 확인(); });
            okno.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            okno.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent dogodek) { 키입력 = true; 확인(); }
            });
            okno.add(Gumb);
            okno.setSize(600, 180);
            okno.setLocation(120, 120);
            okno.setAlwaysOnTop(true);
            okno.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            okno.setVisible(true);
            okno.toFront();
            Timer Pripravi = new Timer(750, dogodek -> {
                Point Položaj = Gumb.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (Položaj.x + Gumb.getWidth() / 2)
                        + " " + (Položaj.y + Gumb.getHeight() / 2));
            });
            Pripravi.setRepeats(false);
            Pripravi.start();
        });
    }
}
