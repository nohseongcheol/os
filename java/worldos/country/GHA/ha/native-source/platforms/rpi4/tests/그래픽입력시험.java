// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame taga;

    private static void Tabbatar_da() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            taga.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window tageti : Window.getWindows()) {
                        if (tageti instanceof JFrame && tageti.isVisible()
                                && ((JFrame) tageti).getTitle().equals("다국어 인사")) {
                            tageti.toFront();
                            new Thread(() -> {
                                try {
                                    Robot daidaita = new Robot();
                                    daidaita.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception Kuskure) {
                                    throw new RuntimeException(Kuskure);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception Kuskure) {
                throw new RuntimeException(Kuskure);
            }
        }
    }

    public static void main(String[] 인수) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            taga = new JFrame("QEMU 키보드·마우스 시험");
            JButton maɓali = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            maɓali.addActionListener(Faruwa -> { 누름 = true; Tabbatar_da(); });
            taga.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            taga.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent Faruwa) { 키입력 = true; Tabbatar_da(); }
            });
            taga.add(maɓali);
            taga.setSize(600, 180);
            taga.setLocation(120, 120);
            taga.setAlwaysOnTop(true);
            taga.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            taga.setVisible(true);
            taga.toFront();
            Timer Shirya = new Timer(750, Faruwa -> {
                Point 위치 = maɓali.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (위치.x + maɓali.getWidth() / 2)
                        + " " + (위치.y + maɓali.getHeight() / 2));
            });
            Shirya.setRepeats(false);
            Shirya.start();
        });
    }
}
