// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame ونڈو;

    private static void تصدیق_کریں() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            ونڈو.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window ہدف : Window.getWindows()) {
                        if (ہدف instanceof JFrame && ہدف.isVisible()
                                && ((JFrame) ہدف).getTitle().equals("다국어 인사")) {
                            ہدف.toFront();
                            new Thread(() -> {
                                try {
                                    Robot ہم_وقت_ساز = new Robot();
                                    ہم_وقت_ساز.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception غلطی) {
                                    throw new RuntimeException(غلطی);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception غلطی) {
                throw new RuntimeException(غلطی);
            }
        }
    }

    public static void main(String[] دلائل) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            ونڈو = new JFrame("QEMU 키보드·마우스 시험");
            JButton بٹن = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            بٹن.addActionListener(واقعہ -> { 누름 = true; تصدیق_کریں(); });
            ونڈو.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            ونڈو.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent واقعہ) { 키입력 = true; تصدیق_کریں(); }
            });
            ونڈو.add(بٹن);
            ونڈو.setSize(600, 180);
            ونڈو.setLocation(120, 120);
            ونڈو.setAlwaysOnTop(true);
            ونڈو.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            ونڈو.setVisible(true);
            ونڈو.toFront();
            Timer تیار_کریں = new Timer(750, واقعہ -> {
                Point مقام = بٹن.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (مقام.x + بٹن.getWidth() / 2)
                        + " " + (مقام.y + بٹن.getHeight() / 2));
            });
            تیار_کریں.setRepeats(false);
            تیار_کریں.start();
        });
    }
}
