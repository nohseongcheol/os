// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, shtyp_VALUE;
    private static JFrame Dritare;

    private static void verifikoj() {
        if (키입력 && shtyp_VALUE) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            Dritare.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window objektiv : Window.getWindows()) {
                        if (objektiv instanceof JFrame && objektiv.isVisible()
                                && ((JFrame) objektiv).getTitle().equals("다국어 인사")) {
                            objektiv.toFront();
                            new Thread(() -> {
                                try {
                                    Robot sinkronizoj = new Robot();
                                    sinkronizoj.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception GABIM) {
                                    throw new RuntimeException(GABIM);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception GABIM) {
                throw new RuntimeException(GABIM);
            }
        }
    }

    public static void main(String[] Argumente) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            Dritare = new JFrame("QEMU 키보드·마우스 시험");
            JButton Buton = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            Buton.addActionListener(Ngjarje -> { shtyp_VALUE = true; verifikoj(); });
            Dritare.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            Dritare.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent Ngjarje) { 키입력 = true; verifikoj(); }
            });
            Dritare.add(Buton);
            Dritare.setSize(600, 180);
            Dritare.setLocation(120, 120);
            Dritare.setAlwaysOnTop(true);
            Dritare.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            Dritare.setVisible(true);
            Dritare.toFront();
            Timer Përgatit = new Timer(750, Ngjarje -> {
                Point Pozicioni = Buton.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (Pozicioni.x + Buton.getWidth() / 2)
                        + " " + (Pozicioni.y + Buton.getHeight() / 2));
            });
            Përgatit.setRepeats(false);
            Përgatit.start();
        });
    }
}
