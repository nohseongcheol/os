// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame uinneag;

    private static void dearbh() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            uinneag.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window targaid : Window.getWindows()) {
                        if (targaid instanceof JFrame && targaid.isVisible()
                                && ((JFrame) targaid).getTitle().equals("다국어 인사")) {
                            targaid.toFront();
                            new Thread(() -> {
                                try {
                                    Robot sioncronaich = new Robot();
                                    sioncronaich.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception Mearachd) {
                                    throw new RuntimeException(Mearachd);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception Mearachd) {
                throw new RuntimeException(Mearachd);
            }
        }
    }

    public static void main(String[] 인수) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            uinneag = new JFrame("QEMU 키보드·마우스 시험");
            JButton putan = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            putan.addActionListener(tachartas -> { 누름 = true; dearbh(); });
            uinneag.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            uinneag.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent tachartas) { 키입력 = true; dearbh(); }
            });
            uinneag.add(putan);
            uinneag.setSize(600, 180);
            uinneag.setLocation(120, 120);
            uinneag.setAlwaysOnTop(true);
            uinneag.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            uinneag.setVisible(true);
            uinneag.toFront();
            Timer Ullaich = new Timer(750, tachartas -> {
                Point suidhich = putan.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (suidhich.x + putan.getWidth() / 2)
                        + " " + (suidhich.y + putan.getHeight() / 2));
            });
            Ullaich.setRepeats(false);
            Ullaich.start();
        });
    }
}
