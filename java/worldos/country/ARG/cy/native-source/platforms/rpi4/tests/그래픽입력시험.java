// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, pwyso_VALUE;
    private static JFrame ffenestr;

    private static void dilysu() {
        if (키입력 && pwyso_VALUE) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            ffenestr.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window targed : Window.getWindows()) {
                        if (targed instanceof JFrame && targed.isVisible()
                                && ((JFrame) targed).getTitle().equals("다국어 인사")) {
                            targed.toFront();
                            new Thread(() -> {
                                try {
                                    Robot cysoni = new Robot();
                                    cysoni.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception Gwall) {
                                    throw new RuntimeException(Gwall);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception Gwall) {
                throw new RuntimeException(Gwall);
            }
        }
    }

    public static void main(String[] 인수) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            ffenestr = new JFrame("QEMU 키보드·마우스 시험");
            JButton botwm = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            botwm.addActionListener(digwyddiad -> { pwyso_VALUE = true; dilysu(); });
            ffenestr.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            ffenestr.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent digwyddiad) { 키입력 = true; dilysu(); }
            });
            ffenestr.add(botwm);
            ffenestr.setSize(600, 180);
            ffenestr.setLocation(120, 120);
            ffenestr.setAlwaysOnTop(true);
            ffenestr.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            ffenestr.setVisible(true);
            ffenestr.toFront();
            Timer Paratoi = new Timer(750, digwyddiad -> {
                Point safle = botwm.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (safle.x + botwm.getWidth() / 2)
                        + " " + (safle.y + botwm.getHeight() / 2));
            });
            Paratoi.setRepeats(false);
            Paratoi.start();
        });
    }
}
