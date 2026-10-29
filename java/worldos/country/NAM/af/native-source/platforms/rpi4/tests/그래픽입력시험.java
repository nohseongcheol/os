// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, druk_VALUE;
    private static JFrame venster;

    private static void verifieer() {
        if (키입력 && druk_VALUE) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            venster.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window teiken : Window.getWindows()) {
                        if (teiken instanceof JFrame && teiken.isVisible()
                                && ((JFrame) teiken).getTitle().equals("다국어 인사")) {
                            teiken.toFront();
                            new Thread(() -> {
                                try {
                                    Robot sinc = new Robot();
                                    sinc.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception Fout) {
                                    throw new RuntimeException(Fout);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception Fout) {
                throw new RuntimeException(Fout);
            }
        }
    }

    public static void main(String[] 인수) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            venster = new JFrame("QEMU 키보드·마우스 시험");
            JButton knoppie = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            knoppie.addActionListener(gebeurtenis -> { druk_VALUE = true; verifieer(); });
            venster.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            venster.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent gebeurtenis) { 키입력 = true; verifieer(); }
            });
            venster.add(knoppie);
            venster.setSize(600, 180);
            venster.setLocation(120, 120);
            venster.setAlwaysOnTop(true);
            venster.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            venster.setVisible(true);
            venster.toFront();
            Timer Maak_gereed = new Timer(750, gebeurtenis -> {
                Point Posisie = knoppie.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (Posisie.x + knoppie.getWidth() / 2)
                        + " " + (Posisie.y + knoppie.getHeight() / 2));
            });
            Maak_gereed.setRepeats(false);
            Maak_gereed.start();
        });
    }
}
