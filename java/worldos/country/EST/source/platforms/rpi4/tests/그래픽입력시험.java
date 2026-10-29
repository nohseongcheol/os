// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, vajutama_VALUE;
    private static JFrame aken;

    private static void kinnitama() {
        if (키입력 && vajutama_VALUE) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            aken.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window siht : Window.getWindows()) {
                        if (siht instanceof JFrame && siht.isVisible()
                                && ((JFrame) siht).getTitle().equals("다국어 인사")) {
                            siht.toFront();
                            new Thread(() -> {
                                try {
                                    Robot sünkroonima = new Robot();
                                    sünkroonima.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception VIGA) {
                                    throw new RuntimeException(VIGA);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception VIGA) {
                throw new RuntimeException(VIGA);
            }
        }
    }

    public static void main(String[] Argumendid) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            aken = new JFrame("QEMU 키보드·마우스 시험");
            JButton nupp = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            nupp.addActionListener(Sündmus -> { vajutama_VALUE = true; kinnitama(); });
            aken.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            aken.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent Sündmus) { 키입력 = true; kinnitama(); }
            });
            aken.add(nupp);
            aken.setSize(600, 180);
            aken.setLocation(120, 120);
            aken.setAlwaysOnTop(true);
            aken.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            aken.setVisible(true);
            aken.toFront();
            Timer Ettevalmistamine = new Timer(750, Sündmus -> {
                Point Asukoht = nupp.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (Asukoht.x + nupp.getWidth() / 2)
                        + " " + (Asukoht.y + nupp.getHeight() / 2));
            });
            Ettevalmistamine.setRepeats(false);
            Ettevalmistamine.start();
        });
    }
}
