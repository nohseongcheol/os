// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame тәрәз;

    private static void раслау() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            тәрәз.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window максат_кыйммәт : Window.getWindows()) {
                        if (максат_кыйммәт instanceof JFrame && максат_кыйммәт.isVisible()
                                && ((JFrame) максат_кыйммәт).getTitle().equals("다국어 인사")) {
                            максат_кыйммәт.toFront();
                            new Thread(() -> {
                                try {
                                    Robot синхронлаштыру = new Robot();
                                    синхронлаштыру.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception Хата) {
                                    throw new RuntimeException(Хата);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception Хата) {
                throw new RuntimeException(Хата);
            }
        }
    }

    public static void main(String[] 인수) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            тәрәз = new JFrame("QEMU 키보드·마우스 시험");
            JButton төймә = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            төймә.addActionListener(вакыйга -> { 누름 = true; раслау(); });
            тәрәз.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            тәрәз.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent вакыйга) { 키입력 = true; раслау(); }
            });
            тәрәз.add(төймә);
            тәрәз.setSize(600, 180);
            тәрәз.setLocation(120, 120);
            тәрәз.setAlwaysOnTop(true);
            тәрәз.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            тәрәз.setVisible(true);
            тәрәз.toFront();
            Timer Әзерләү = new Timer(750, вакыйга -> {
                Point урнаштыру = төймә.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (урнаштыру.x + төймә.getWidth() / 2)
                        + " " + (урнаштыру.y + төймә.getHeight() / 2));
            });
            Әзерләү.setRepeats(false);
            Әзерләү.start();
        });
    }
}
