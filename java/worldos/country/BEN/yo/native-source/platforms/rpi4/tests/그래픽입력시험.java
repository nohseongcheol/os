// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame wínńdò;

    private static void ridájú() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            wínńdò.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window àfojúsùn : Window.getWindows()) {
                        if (àfojúsùn instanceof JFrame && àfojúsùn.isVisible()
                                && ((JFrame) àfojúsùn).getTitle().equals("다국어 인사")) {
                            àfojúsùn.toFront();
                            new Thread(() -> {
                                try {
                                    Robot múdọ́gba = new Robot();
                                    múdọ́gba.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception àṣìṣe) {
                                    throw new RuntimeException(àṣìṣe);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception àṣìṣe) {
                throw new RuntimeException(àṣìṣe);
            }
        }
    }

    public static void main(String[] 인수) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            wínńdò = new JFrame("QEMU 키보드·마우스 시험");
            JButton bọ́tìnnì = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            bọ́tìnnì.addActionListener(ìgbéṣẹ̀ -> { 누름 = true; ridájú(); });
            wínńdò.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            wínńdò.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent ìgbéṣẹ̀) { 키입력 = true; ridájú(); }
            });
            wínńdò.add(bọ́tìnnì);
            wínńdò.setSize(600, 180);
            wínńdò.setLocation(120, 120);
            wínńdò.setAlwaysOnTop(true);
            wínńdò.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            wínńdò.setVisible(true);
            wínńdò.toFront();
            Timer gbaradì = new Timer(750, ìgbéṣẹ̀ -> {
                Point 위치 = bọ́tìnnì.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (위치.x + bọ́tìnnì.getWidth() / 2)
                        + " " + (위치.y + bọ́tìnnì.getHeight() / 2));
            });
            gbaradì.setRepeats(false);
            gbaradì.start();
        });
    }
}
