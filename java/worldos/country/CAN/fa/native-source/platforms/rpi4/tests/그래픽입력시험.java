// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, فشار_دادن_مقدار;
    private static JFrame پنجره;

    private static void تأیید_صحت() {
        if (키입력 && فشار_دادن_مقدار) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            پنجره.dispose();
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
                                    Robot همگام_سازی = new Robot();
                                    همگام_سازی.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception خطا) {
                                    throw new RuntimeException(خطا);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception خطا) {
                throw new RuntimeException(خطا);
            }
        }
    }

    public static void main(String[] نشانوندها) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            پنجره = new JFrame("QEMU 키보드·마우스 시험");
            JButton دکمه = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            دکمه.addActionListener(رویداد -> { فشار_دادن_مقدار = true; تأیید_صحت(); });
            پنجره.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            پنجره.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent رویداد) { 키입력 = true; تأیید_صحت(); }
            });
            پنجره.add(دکمه);
            پنجره.setSize(600, 180);
            پنجره.setLocation(120, 120);
            پنجره.setAlwaysOnTop(true);
            پنجره.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            پنجره.setVisible(true);
            پنجره.toFront();
            Timer آماده_کردن = new Timer(750, رویداد -> {
                Point مرتب_کردن = دکمه.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (مرتب_کردن.x + دکمه.getWidth() / 2)
                        + " " + (مرتب_کردن.y + دکمه.getHeight() / 2));
            });
            آماده_کردن.setRepeats(false);
            آماده_کردن.start();
        });
    }
}
