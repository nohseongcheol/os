// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, დაჭერა_მნიშვნელობა;
    private static JFrame ფანჯარა;

    private static void გადამოწმება() {
        if (키입력 && დაჭერა_მნიშვნელობა) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            ფანჯარა.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window მიზანი : Window.getWindows()) {
                        if (მიზანი instanceof JFrame && მიზანი.isVisible()
                                && ((JFrame) მიზანი).getTitle().equals("다국어 인사")) {
                            მიზანი.toFront();
                            new Thread(() -> {
                                try {
                                    Robot დასინქრონება = new Robot();
                                    დასინქრონება.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception შეცდომა) {
                                    throw new RuntimeException(შეცდომა);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception შეცდომა) {
                throw new RuntimeException(შეცდომა);
            }
        }
    }

    public static void main(String[] 인수) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            ფანჯარა = new JFrame("QEMU 키보드·마우스 시험");
            JButton ღილაკი = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            ღილაკი.addActionListener(მოვლენა -> { დაჭერა_მნიშვნელობა = true; გადამოწმება(); });
            ფანჯარა.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            ფანჯარა.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent მოვლენა) { 키입력 = true; გადამოწმება(); }
            });
            ფანჯარა.add(ღილაკი);
            ფანჯარა.setSize(600, 180);
            ფანჯარა.setLocation(120, 120);
            ფანჯარა.setAlwaysOnTop(true);
            ფანჯარა.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            ფანჯარა.setVisible(true);
            ფანჯარა.toFront();
            Timer მომზადება = new Timer(750, მოვლენა -> {
                Point პოზიცია = ღილაკი.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (პოზიცია.x + ღილაკი.getWidth() / 2)
                        + " " + (პოზიცია.y + ღილაკი.getHeight() / 2));
            });
            მომზადება.setRepeats(false);
            მომზადება.start();
        });
    }
}
