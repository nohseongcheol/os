// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame دري;

    private static void تصديق_ڪريو() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            دري.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window هدف : Window.getWindows()) {
                        if (هدف instanceof JFrame && هدف.isVisible()
                                && ((JFrame) هدف).getTitle().equals("다국어 인사")) {
                            هدف.toFront();
                            new Thread(() -> {
                                try {
                                    Robot هم_وقت = new Robot();
                                    هم_وقت.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception نقص) {
                                    throw new RuntimeException(نقص);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception نقص) {
                throw new RuntimeException(نقص);
            }
        }
    }

    public static void main(String[] 인수) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            دري = new JFrame("QEMU 키보드·마우스 시험");
            JButton بٽن = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            بٽن.addActionListener(واقعو -> { 누름 = true; تصديق_ڪريو(); });
            دري.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            دري.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent واقعو) { 키입력 = true; تصديق_ڪريو(); }
            });
            دري.add(بٽن);
            دري.setSize(600, 180);
            دري.setLocation(120, 120);
            دري.setAlwaysOnTop(true);
            دري.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            دري.setVisible(true);
            دري.toFront();
            Timer تياري_ڪريو = new Timer(750, واقعو -> {
                Point 위치 = بٽن.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (위치.x + بٽن.getWidth() / 2)
                        + " " + (위치.y + بٽن.getHeight() / 2));
            });
            تياري_ڪريو.setRepeats(false);
            تياري_ڪريو.start();
        });
    }
}
