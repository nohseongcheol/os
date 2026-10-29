// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame palanteer;

    private static void luñutu() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            palanteer.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window luñu_name : Window.getWindows()) {
                        if (luñu_name instanceof JFrame && luñu_name.isVisible()
                                && ((JFrame) luñu_name).getTitle().equals("다국어 인사")) {
                            luñu_name.toFront();
                            new Thread(() -> {
                                try {
                                    Robot lëkkale = new Robot();
                                    lëkkale.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception njumte) {
                                    throw new RuntimeException(njumte);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception njumte) {
                throw new RuntimeException(njumte);
            }
        }
    }

    public static void main(String[] 인수) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            palanteer = new JFrame("QEMU 키보드·마우스 시험");
            JButton butoñ = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            butoñ.addActionListener(xewxew -> { 누름 = true; luñutu(); });
            palanteer.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            palanteer.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent xewxew) { 키입력 = true; luñutu(); }
            });
            palanteer.add(butoñ);
            palanteer.setSize(600, 180);
            palanteer.setLocation(120, 120);
            palanteer.setAlwaysOnTop(true);
            palanteer.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            palanteer.setVisible(true);
            palanteer.toFront();
            Timer jël_matuwaay = new Timer(750, xewxew -> {
                Point 위치 = butoñ.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (위치.x + butoñ.getWidth() / 2)
                        + " " + (위치.y + butoñ.getHeight() / 2));
            });
            jël_matuwaay.setRepeats(false);
            jël_matuwaay.start();
        });
    }
}
