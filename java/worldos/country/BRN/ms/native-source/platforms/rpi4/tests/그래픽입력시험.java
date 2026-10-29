// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, tekan_VALUE;
    private static JFrame Tetingkap;

    private static void tentu_sahkan() {
        if (키입력 && tekan_VALUE) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            Tetingkap.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window sasaran : Window.getWindows()) {
                        if (sasaran instanceof JFrame && sasaran.isVisible()
                                && ((JFrame) sasaran).getTitle().equals("다국어 인사")) {
                            sasaran.toFront();
                            new Thread(() -> {
                                try {
                                    Robot segerak = new Robot();
                                    segerak.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception RALAT) {
                                    throw new RuntimeException(RALAT);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception RALAT) {
                throw new RuntimeException(RALAT);
            }
        }
    }

    public static void main(String[] 인수) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            Tetingkap = new JFrame("QEMU 키보드·마우스 ujian");
            JButton Butang = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            Butang.addActionListener(Peristiwa -> { tekan_VALUE = true; tentu_sahkan(); });
            Tetingkap.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            Tetingkap.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent Peristiwa) { 키입력 = true; tentu_sahkan(); }
            });
            Tetingkap.add(Butang);
            Tetingkap.setSize(600, 180);
            Tetingkap.setLocation(120, 120);
            Tetingkap.setAlwaysOnTop(true);
            Tetingkap.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            Tetingkap.setVisible(true);
            Tetingkap.toFront();
            Timer Sediakan = new Timer(750, Peristiwa -> {
                Point Kedudukan = Butang.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (Kedudukan.x + Butang.getWidth() / 2)
                        + " " + (Kedudukan.y + Butang.getHeight() / 2));
            });
            Sediakan.setRepeats(false);
            Sediakan.start();
        });
    }
}
