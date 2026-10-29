// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame idirishya;

    private static void gusuzuma() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            idirishya.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window gusimbuza_igishya : Window.getWindows()) {
                        if (gusimbuza_igishya instanceof JFrame && gusimbuza_igishya.isVisible()
                                && ((JFrame) gusimbuza_igishya).getTitle().equals("다국어 인사")) {
                            gusimbuza_igishya.toFront();
                            new Thread(() -> {
                                try {
                                    Robot guhuza = new Robot();
                                    guhuza.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception IKOSA) {
                                    throw new RuntimeException(IKOSA);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception IKOSA) {
                throw new RuntimeException(IKOSA);
            }
        }
    }

    public static void main(String[] 인수) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            idirishya = new JFrame("QEMU 키보드·마우스 시험");
            JButton buto = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            buto.addActionListener(icyabaye -> { 누름 = true; gusuzuma(); });
            idirishya.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            idirishya.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent icyabaye) { 키입력 = true; gusuzuma(); }
            });
            idirishya.add(buto);
            idirishya.setSize(600, 180);
            idirishya.setLocation(120, 120);
            idirishya.setAlwaysOnTop(true);
            idirishya.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            idirishya.setVisible(true);
            idirishya.toFront();
            Timer Gutegura = new Timer(750, icyabaye -> {
                Point 위치 = buto.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (위치.x + buto.getWidth() / 2)
                        + " " + (위치.y + buto.getHeight() / 2));
            });
            Gutegura.setRepeats(false);
            Gutegura.start();
        });
    }
}
