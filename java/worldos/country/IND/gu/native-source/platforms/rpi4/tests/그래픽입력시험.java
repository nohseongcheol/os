// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame વિંડો;

    private static void ચકાસવું() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            વિંડો.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window લક્ષ્ય : Window.getWindows()) {
                        if (લક્ષ્ય instanceof JFrame && લક્ષ્ય.isVisible()
                                && ((JFrame) લક્ષ્ય).getTitle().equals("다국어 인사")) {
                            લક્ષ્ય.toFront();
                            new Thread(() -> {
                                try {
                                    Robot સિંક્રનાઇઝ = new Robot();
                                    સિંક્રનાઇઝ.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception ભૂલ) {
                                    throw new RuntimeException(ભૂલ);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception ભૂલ) {
                throw new RuntimeException(ભૂલ);
            }
        }
    }

    public static void main(String[] દલીલો) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            વિંડો = new JFrame("QEMU 키보드·마우스 시험");
            JButton બટન = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            બટન.addActionListener(ઇવેંટ -> { 누름 = true; ચકાસવું(); });
            વિંડો.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            વિંડો.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent ઇવેંટ) { 키입력 = true; ચકાસવું(); }
            });
            વિંડો.add(બટન);
            વિંડો.setSize(600, 180);
            વિંડો.setLocation(120, 120);
            વિંડો.setAlwaysOnTop(true);
            વિંડો.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            વિંડો.setVisible(true);
            વિંડો.toFront();
            Timer તૈયાર_કરો = new Timer(750, ઇવેંટ -> {
                Point સ્થાન = બટન.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (સ્થાન.x + બટન.getWidth() / 2)
                        + " " + (સ્થાન.y + બટન.getHeight() / 2));
            });
            તૈયાર_કરો.setRepeats(false);
            તૈયાર_કરો.start();
        });
    }
}
