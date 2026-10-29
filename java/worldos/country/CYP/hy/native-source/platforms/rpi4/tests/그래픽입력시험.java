// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame պատուհան;

    private static void հաստատել() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            պատուհան.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window թիրախ : Window.getWindows()) {
                        if (թիրախ instanceof JFrame && թիրախ.isVisible()
                                && ((JFrame) թիրախ).getTitle().equals("다국어 인사")) {
                            թիրախ.toFront();
                            new Thread(() -> {
                                try {
                                    Robot համաժամել = new Robot();
                                    համաժամել.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception Սխալ) {
                                    throw new RuntimeException(Սխալ);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception Սխալ) {
                throw new RuntimeException(Սխալ);
            }
        }
    }

    public static void main(String[] 인수) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            պատուհան = new JFrame("QEMU 키보드·마우스 시험");
            JButton կոճակ = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            կոճակ.addActionListener(միջոցառում -> { 누름 = true; հաստատել(); });
            պատուհան.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            պատուհան.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent միջոցառում) { 키입력 = true; հաստատել(); }
            });
            պատուհան.add(կոճակ);
            պատուհան.setSize(600, 180);
            պատուհան.setLocation(120, 120);
            պատուհան.setAlwaysOnTop(true);
            պատուհան.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            պատուհան.setVisible(true);
            պատուհան.toFront();
            Timer Պատրաստել = new Timer(750, միջոցառում -> {
                Point Դիրք = կոճակ.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (Դիրք.x + կոճակ.getWidth() / 2)
                        + " " + (Դիրք.y + կոճակ.getHeight() / 2));
            });
            Պատրաստել.setRepeats(false);
            Պատրաստել.start();
        });
    }
}
