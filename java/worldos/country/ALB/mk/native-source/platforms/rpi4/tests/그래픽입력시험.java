// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame прозорец;

    private static void провери() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            прозорец.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window цел : Window.getWindows()) {
                        if (цел instanceof JFrame && цел.isVisible()
                                && ((JFrame) цел).getTitle().equals("다국어 인사")) {
                            цел.toFront();
                            new Thread(() -> {
                                try {
                                    Robot синхронизирај = new Robot();
                                    синхронизирај.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception ГРЕШКА) {
                                    throw new RuntimeException(ГРЕШКА);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception ГРЕШКА) {
                throw new RuntimeException(ГРЕШКА);
            }
        }
    }

    public static void main(String[] Аргументи) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            прозорец = new JFrame("QEMU 키보드·마우스 시험");
            JButton копче = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            копче.addActionListener(настан -> { 누름 = true; провери(); });
            прозорец.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            прозорец.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent настан) { 키입력 = true; провери(); }
            });
            прозорец.add(копче);
            прозорец.setSize(600, 180);
            прозорец.setLocation(120, 120);
            прозорец.setAlwaysOnTop(true);
            прозорец.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            прозорец.setVisible(true);
            прозорец.toFront();
            Timer Подготви = new Timer(750, настан -> {
                Point Позиција = копче.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (Позиција.x + копче.getWidth() / 2)
                        + " " + (Позиција.y + копче.getHeight() / 2));
            });
            Подготви.setRepeats(false);
            Подготви.start();
        });
    }
}
