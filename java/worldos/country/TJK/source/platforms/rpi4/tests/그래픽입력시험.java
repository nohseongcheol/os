// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame равзана;

    private static void тасдиқ_кардан() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            равзана.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window ҳадаф : Window.getWindows()) {
                        if (ҳадаф instanceof JFrame && ҳадаф.isVisible()
                                && ((JFrame) ҳадаф).getTitle().equals("다국어 인사")) {
                            ҳадаф.toFront();
                            new Thread(() -> {
                                try {
                                    Robot ҳамоҳанг_кардан = new Robot();
                                    ҳамоҳанг_кардан.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception Хато) {
                                    throw new RuntimeException(Хато);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception Хато) {
                throw new RuntimeException(Хато);
            }
        }
    }

    public static void main(String[] 인수) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            равзана = new JFrame("QEMU 키보드·마우스 시험");
            JButton тугма = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            тугма.addActionListener(рӯйдод -> { 누름 = true; тасдиқ_кардан(); });
            равзана.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            равзана.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent рӯйдод) { 키입력 = true; тасдиқ_кардан(); }
            });
            равзана.add(тугма);
            равзана.setSize(600, 180);
            равзана.setLocation(120, 120);
            равзана.setAlwaysOnTop(true);
            равзана.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            равзана.setVisible(true);
            равзана.toFront();
            Timer Омода_кардан = new Timer(750, рӯйдод -> {
                Point 위치 = тугма.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (위치.x + тугма.getWidth() / 2)
                        + " " + (위치.y + тугма.getHeight() / 2));
            });
            Омода_кардан.setRepeats(false);
            Омода_кардан.start();
        });
    }
}
