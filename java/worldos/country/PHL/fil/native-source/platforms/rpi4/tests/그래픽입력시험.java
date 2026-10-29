// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame window;

    private static void tiyakin_kumpirmahin() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            window.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window layunin : Window.getWindows()) {
                        if (layunin instanceof JFrame && layunin.isVisible()
                                && ((JFrame) layunin).getTitle().equals("다국어 인사")) {
                            layunin.toFront();
                            new Thread(() -> {
                                try {
                                    Robot iakma = new Robot();
                                    iakma.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception error) {
                                    throw new RuntimeException(error);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception error) {
                throw new RuntimeException(error);
            }
        }
    }

    public static void main(String[] 인수) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            window = new JFrame("QEMU 키보드·마우스 시험");
            JButton button = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            button.addActionListener(kaganapan -> { 누름 = true; tiyakin_kumpirmahin(); });
            window.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            window.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent kaganapan) { 키입력 = true; tiyakin_kumpirmahin(); }
            });
            window.add(button);
            window.setSize(600, 180);
            window.setLocation(120, 120);
            window.setAlwaysOnTop(true);
            window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            window.setVisible(true);
            window.toFront();
            Timer Ihanda = new Timer(750, kaganapan -> {
                Point posisyon = button.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (posisyon.x + button.getWidth() / 2)
                        + " " + (posisyon.y + button.getHeight() / 2));
            });
            Ihanda.setRepeats(false);
            Ihanda.start();
        });
    }
}
