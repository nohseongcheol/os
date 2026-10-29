// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame پەنجەرە;

    private static void سەلماندن() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            پەنجەرە.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window مەبەست : Window.getWindows()) {
                        if (مەبەست instanceof JFrame && مەبەست.isVisible()
                                && ((JFrame) مەبەست).getTitle().equals("다국어 인사")) {
                            مەبەست.toFront();
                            new Thread(() -> {
                                try {
                                    Robot هاودەمکردن = new Robot();
                                    هاودەمکردن.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception هەڵە) {
                                    throw new RuntimeException(هەڵە);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception هەڵە) {
                throw new RuntimeException(هەڵە);
            }
        }
    }

    public static void main(String[] 인수) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            پەنجەرە = new JFrame("QEMU 키보드·마우스 시험");
            JButton دوگمه = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            دوگمه.addActionListener(پێشهات -> { 누름 = true; سەلماندن(); });
            پەنجەرە.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            پەنجەرە.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent پێشهات) { 키입력 = true; سەلماندن(); }
            });
            پەنجەرە.add(دوگمه);
            پەنجەرە.setSize(600, 180);
            پەنجەرە.setLocation(120, 120);
            پەنجەرە.setAlwaysOnTop(true);
            پەنجەرە.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            پەنجەرە.setVisible(true);
            پەنجەرە.toFront();
            Timer ئامادە_کردن_9ce364fc = new Timer(750, پێشهات -> {
                Point 위치 = دوگمه.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (위치.x + دوگمه.getWidth() / 2)
                        + " " + (위치.y + دوگمه.getHeight() / 2));
            });
            ئامادە_کردن_9ce364fc.setRepeats(false);
            ئامادە_کردن_9ce364fc.start();
        });
    }
}
