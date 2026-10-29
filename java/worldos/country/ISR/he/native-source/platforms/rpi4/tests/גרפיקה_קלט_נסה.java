// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class גרפיקה_קלט_נסה {
    private static boolean מקש_קלט, 누름;
    private static JFrame חלון;

    private static void ודא_אמת() {
        if (מקש_קלט && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            חלון.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window יעד : Window.getWindows()) {
                        if (יעד instanceof JFrame && יעד.isVisible()
                                && ((JFrame) יעד).getTitle().equals("다국어 인사")) {
                            יעד.toFront();
                            new Thread(() -> {
                                try {
                                    Robot סנכרן = new Robot();
                                    סנכרן.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception שגיאה) {
                                    throw new RuntimeException(שגיאה);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception שגיאה) {
                throw new RuntimeException(שגיאה);
            }
        }
    }

    public static void main(String[] ארגומנטים) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            חלון = new JFrame("QEMU 키보드·마우스 시험");
            JButton לחצן = new JButton("한글 화면 · 이 단추를 누르고 K를 קלט_ערך");
            לחצן.addActionListener(אירוע -> { 누름 = true; ודא_אמת(); });
            חלון.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            חלון.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent אירוע) { מקש_קלט = true; ודא_אמת(); }
            });
            חלון.add(לחצן);
            חלון.setSize(600, 180);
            חלון.setLocation(120, 120);
            חלון.setAlwaysOnTop(true);
            חלון.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            חלון.setVisible(true);
            חלון.toFront();
            Timer להכין = new Timer(750, אירוע -> {
                Point מיקום = לחצן.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (מיקום.x + לחצן.getWidth() / 2)
                        + " " + (מיקום.y + לחצן.getHeight() / 2));
            });
            להכין.setRepeats(false);
            להכין.start();
        });
    }
}
