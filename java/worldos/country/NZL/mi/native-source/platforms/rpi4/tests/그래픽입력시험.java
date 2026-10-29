// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame matapihi;

    private static void manatoko() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            matapihi.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window ūnga : Window.getWindows()) {
                        if (ūnga instanceof JFrame && ūnga.isVisible()
                                && ((JFrame) ūnga).getTitle().equals("다국어 인사")) {
                            ūnga.toFront();
                            new Thread(() -> {
                                try {
                                    Robot tukutahi = new Robot();
                                    tukutahi.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception Pōhēhē) {
                                    throw new RuntimeException(Pōhēhē);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception Pōhēhē) {
                throw new RuntimeException(Pōhēhē);
            }
        }
    }

    public static void main(String[] 인수) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            matapihi = new JFrame("QEMU 키보드·마우스 시험");
            JButton pātene = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            pātene.addActionListener(hui -> { 누름 = true; manatoko(); });
            matapihi.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            matapihi.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent hui) { 키입력 = true; manatoko(); }
            });
            matapihi.add(pātene);
            matapihi.setSize(600, 180);
            matapihi.setLocation(120, 120);
            matapihi.setAlwaysOnTop(true);
            matapihi.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            matapihi.setVisible(true);
            matapihi.toFront();
            Timer Whakarite = new Timer(750, hui -> {
                Point tūranga = pātene.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (tūranga.x + pātene.getWidth() / 2)
                        + " " + (tūranga.y + pātene.getHeight() / 2));
            });
            Whakarite.setRepeats(false);
            Whakarite.start();
        });
    }
}
