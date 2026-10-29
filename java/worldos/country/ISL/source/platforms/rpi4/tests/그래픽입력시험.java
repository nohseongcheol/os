// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, ýta_VALUE;
    private static JFrame Gluggi;

    private static void sannprófa() {
        if (키입력 && ýta_VALUE) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            Gluggi.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window markmið : Window.getWindows()) {
                        if (markmið instanceof JFrame && markmið.isVisible()
                                && ((JFrame) markmið).getTitle().equals("다국어 인사")) {
                            markmið.toFront();
                            new Thread(() -> {
                                try {
                                    Robot samstilla = new Robot();
                                    samstilla.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception Villa) {
                                    throw new RuntimeException(Villa);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception Villa) {
                throw new RuntimeException(Villa);
            }
        }
    }

    public static void main(String[] Viðföng) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            Gluggi = new JFrame("QEMU 키보드·마우스 시험");
            JButton hnappur = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            hnappur.addActionListener(atvik -> { ýta_VALUE = true; sannprófa(); });
            Gluggi.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            Gluggi.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent atvik) { 키입력 = true; sannprófa(); }
            });
            Gluggi.add(hnappur);
            Gluggi.setSize(600, 180);
            Gluggi.setLocation(120, 120);
            Gluggi.setAlwaysOnTop(true);
            Gluggi.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            Gluggi.setVisible(true);
            Gluggi.toFront();
            Timer Undirbúa = new Timer(750, atvik -> {
                Point Staðsetning = hnappur.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (Staðsetning.x + hnappur.getWidth() / 2)
                        + " " + (Staðsetning.y + hnappur.getHeight() / 2));
            });
            Undirbúa.setRepeats(false);
            Undirbúa.start();
        });
    }
}
