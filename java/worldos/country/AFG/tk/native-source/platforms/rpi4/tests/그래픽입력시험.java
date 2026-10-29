// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame penjire;

    private static void barla() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            penjire.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window niýet : Window.getWindows()) {
                        if (niýet instanceof JFrame && niýet.isVisible()
                                && ((JFrame) niýet).getTitle().equals("다국어 인사")) {
                            niýet.toFront();
                            new Thread(() -> {
                                try {
                                    Robot sinhronlaşdyr = new Robot();
                                    sinhronlaşdyr.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception Hata) {
                                    throw new RuntimeException(Hata);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception Hata) {
                throw new RuntimeException(Hata);
            }
        }
    }

    public static void main(String[] 인수) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            penjire = new JFrame("QEMU 키보드·마우스 시험");
            JButton düwme = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            düwme.addActionListener(waka -> { 누름 = true; barla(); });
            penjire.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            penjire.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent waka) { 키입력 = true; barla(); }
            });
            penjire.add(düwme);
            penjire.setSize(600, 180);
            penjire.setLocation(120, 120);
            penjire.setAlwaysOnTop(true);
            penjire.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            penjire.setVisible(true);
            penjire.toFront();
            Timer Taýýarla = new Timer(750, waka -> {
                Point 위치 = düwme.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (위치.x + düwme.getWidth() / 2)
                        + " " + (위치.y + düwme.getHeight() / 2));
            });
            Taýýarla.setRepeats(false);
            Taýýarla.start();
        });
    }
}
