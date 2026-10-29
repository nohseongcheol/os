// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame oyna;

    private static void tasdiqlamoq() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            oyna.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window nishon : Window.getWindows()) {
                        if (nishon instanceof JFrame && nishon.isVisible()
                                && ((JFrame) nishon).getTitle().equals("다국어 인사")) {
                            nishon.toFront();
                            new Thread(() -> {
                                try {
                                    Robot sinxronlashtirish = new Robot();
                                    sinxronlashtirish.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception Xato) {
                                    throw new RuntimeException(Xato);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception Xato) {
                throw new RuntimeException(Xato);
            }
        }
    }

    public static void main(String[] 인수) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            oyna = new JFrame("QEMU 키보드·마우스 시험");
            JButton tugma = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            tugma.addActionListener(hodisa -> { 누름 = true; tasdiqlamoq(); });
            oyna.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            oyna.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent hodisa) { 키입력 = true; tasdiqlamoq(); }
            });
            oyna.add(tugma);
            oyna.setSize(600, 180);
            oyna.setLocation(120, 120);
            oyna.setAlwaysOnTop(true);
            oyna.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            oyna.setVisible(true);
            oyna.toFront();
            Timer Tayyorlamoq = new Timer(750, hodisa -> {
                Point Holati = tugma.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (Holati.x + tugma.getWidth() / 2)
                        + " " + (Holati.y + tugma.getHeight() / 2));
            });
            Tayyorlamoq.setRepeats(false);
            Tayyorlamoq.start();
        });
    }
}
