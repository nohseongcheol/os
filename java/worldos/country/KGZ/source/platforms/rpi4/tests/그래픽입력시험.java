// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame терезе;

    private static void тууралыгын_аныктоо() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            терезе.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window максат : Window.getWindows()) {
                        if (максат instanceof JFrame && максат.isVisible()
                                && ((JFrame) максат).getTitle().equals("다국어 인사")) {
                            максат.toFront();
                            new Thread(() -> {
                                try {
                                    Robot синхрондоштуруу = new Robot();
                                    синхрондоштуруу.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception Ката) {
                                    throw new RuntimeException(Ката);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception Ката) {
                throw new RuntimeException(Ката);
            }
        }
    }

    public static void main(String[] 인수) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            терезе = new JFrame("QEMU 키보드·마우스 시험");
            JButton баскыч = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            баскыч.addActionListener(окуя -> { 누름 = true; тууралыгын_аныктоо(); });
            терезе.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            терезе.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent окуя) { 키입력 = true; тууралыгын_аныктоо(); }
            });
            терезе.add(баскыч);
            терезе.setSize(600, 180);
            терезе.setLocation(120, 120);
            терезе.setAlwaysOnTop(true);
            терезе.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            терезе.setVisible(true);
            терезе.toFront();
            Timer Даярдоо = new Timer(750, окуя -> {
                Point Турган_жери = баскыч.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (Турган_жери.x + баскыч.getWidth() / 2)
                        + " " + (Турган_жери.y + баскыч.getHeight() / 2));
            });
            Даярдоо.setRepeats(false);
            Даярдоо.start();
        });
    }
}
