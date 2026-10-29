// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, bas_VALUE;
    private static JFrame pəncərə;

    private static void yoxlamaq() {
        if (키입력 && bas_VALUE) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            pəncərə.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window hədəf : Window.getWindows()) {
                        if (hədəf instanceof JFrame && hədəf.isVisible()
                                && ((JFrame) hədəf).getTitle().equals("다국어 인사")) {
                            hədəf.toFront();
                            new Thread(() -> {
                                try {
                                    Robot sinxronlaşdırmaq = new Robot();
                                    sinxronlaşdırmaq.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception XƏTA) {
                                    throw new RuntimeException(XƏTA);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception XƏTA) {
                throw new RuntimeException(XƏTA);
            }
        }
    }

    public static void main(String[] 인수) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            pəncərə = new JFrame("QEMU 키보드·마우스 시험");
            JButton düymə = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            düymə.addActionListener(hadisə -> { bas_VALUE = true; yoxlamaq(); });
            pəncərə.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            pəncərə.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent hadisə) { 키입력 = true; yoxlamaq(); }
            });
            pəncərə.add(düymə);
            pəncərə.setSize(600, 180);
            pəncərə.setLocation(120, 120);
            pəncərə.setAlwaysOnTop(true);
            pəncərə.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            pəncərə.setVisible(true);
            pəncərə.toFront();
            Timer Hazırla = new Timer(750, hadisə -> {
                Point yerinə_qoymaq = düymə.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (yerinə_qoymaq.x + düymə.getWidth() / 2)
                        + " " + (yerinə_qoymaq.y + düymə.getHeight() / 2));
            });
            Hazırla.setRepeats(false);
            Hazırla.start();
        });
    }
}
