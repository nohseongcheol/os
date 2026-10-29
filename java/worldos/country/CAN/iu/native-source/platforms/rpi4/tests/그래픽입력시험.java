// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame igalaangujaq;

    private static void nalunairli_1aacb54c() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            igalaangujaq.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window turaagaq : Window.getWindows()) {
                        if (turaagaq instanceof JFrame && turaagaq.isVisible()
                                && ((JFrame) turaagaq).getTitle().equals("다국어 인사")) {
                            turaagaq.toFront();
                            new Thread(() -> {
                                try {
                                    Robot asiqqunniqannginniq = new Robot();
                                    asiqqunniqannginniq.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception tammarniq) {
                                    throw new RuntimeException(tammarniq);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception tammarniq) {
                throw new RuntimeException(tammarniq);
            }
        }
    }

    public static void main(String[] 인수) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            igalaangujaq = new JFrame("QEMU 키보드·마우스 시험");
            JButton tikkuagaq = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            tikkuagaq.addActionListener(piniku -> { 누름 = true; nalunairli_1aacb54c(); });
            igalaangujaq.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            igalaangujaq.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent piniku) { 키입력 = true; nalunairli_1aacb54c(); }
            });
            igalaangujaq.add(tikkuagaq);
            igalaangujaq.setSize(600, 180);
            igalaangujaq.setLocation(120, 120);
            igalaangujaq.setAlwaysOnTop(true);
            igalaangujaq.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            igalaangujaq.setVisible(true);
            igalaangujaq.toFront();
            Timer Parnalli = new Timer(750, piniku -> {
                Point 위치 = tikkuagaq.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (위치.x + tikkuagaq.getWidth() / 2)
                        + " " + (위치.y + tikkuagaq.getHeight() / 2));
            });
            Parnalli.setRepeats(false);
            Parnalli.start();
        });
    }
}
