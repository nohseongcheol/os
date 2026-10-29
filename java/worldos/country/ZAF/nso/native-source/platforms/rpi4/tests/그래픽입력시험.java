// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame lefastere;

    private static void kgonthiša() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            lefastere.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window nepo : Window.getWindows()) {
                        if (nepo instanceof JFrame && nepo.isVisible()
                                && ((JFrame) nepo).getTitle().equals("다국어 인사")) {
                            nepo.toFront();
                            new Thread(() -> {
                                try {
                                    Robot kopanya = new Robot();
                                    kopanya.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception Phošo) {
                                    throw new RuntimeException(Phošo);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception Phošo) {
                throw new RuntimeException(Phošo);
            }
        }
    }

    public static void main(String[] 인수) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            lefastere = new JFrame("QEMU 키보드·마우스 시험");
            JButton konope = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            konope.addActionListener(tiragalo -> { 누름 = true; kgonthiša(); });
            lefastere.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            lefastere.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent tiragalo) { 키입력 = true; kgonthiša(); }
            });
            lefastere.add(konope);
            lefastere.setSize(600, 180);
            lefastere.setLocation(120, 120);
            lefastere.setAlwaysOnTop(true);
            lefastere.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            lefastere.setVisible(true);
            lefastere.toFront();
            Timer Lokišetša = new Timer(750, tiragalo -> {
                Point 위치 = konope.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (위치.x + konope.getWidth() / 2)
                        + " " + (위치.y + konope.getHeight() / 2));
            });
            Lokišetša.setRepeats(false);
            Lokišetša.start();
        });
    }
}
