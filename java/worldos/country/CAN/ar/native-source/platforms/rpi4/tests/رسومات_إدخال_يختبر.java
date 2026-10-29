// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class رسومات_إدخال_يختبر {
    private static boolean مفتاح_إدخال, 누름;
    private static JFrame نافذة;

    private static void يتحقق() {
        if (مفتاح_إدخال && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            نافذة.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window الهدف : Window.getWindows()) {
                        if (الهدف instanceof JFrame && الهدف.isVisible()
                                && ((JFrame) الهدف).getTitle().equals("다국어 인사")) {
                            الهدف.toFront();
                            new Thread(() -> {
                                try {
                                    Robot تزامن = new Robot();
                                    تزامن.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception خطأ) {
                                    throw new RuntimeException(خطأ);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception خطأ) {
                throw new RuntimeException(خطأ);
            }
        }
    }

    public static void main(String[] وسائط) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            نافذة = new JFrame("QEMU 키보드·마우스 اختبارات");
            JButton زر = new JButton("한글 화면 · 이 단추를 누르고 K를 إدخال_قيمة");
            زر.addActionListener(حدث -> { 누름 = true; يتحقق(); });
            نافذة.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            نافذة.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent حدث) { مفتاح_إدخال = true; يتحقق(); }
            });
            نافذة.add(زر);
            نافذة.setSize(600, 180);
            نافذة.setLocation(120, 120);
            نافذة.setAlwaysOnTop(true);
            نافذة.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            نافذة.setVisible(true);
            نافذة.toFront();
            Timer إعداد = new Timer(750, حدث -> {
                Point موضع = زر.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (موضع.x + زر.getWidth() / 2)
                        + " " + (موضع.y + زر.getHeight() / 2));
            });
            إعداد.setRepeats(false);
            إعداد.start();
        });
    }
}
