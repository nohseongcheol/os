// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame విండో;

    private static void సరిచూడు() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            విండో.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window లక్ష్యం : Window.getWindows()) {
                        if (లక్ష్యం instanceof JFrame && లక్ష్యం.isVisible()
                                && ((JFrame) లక్ష్యం).getTitle().equals("다국어 인사")) {
                            లక్ష్యం.toFront();
                            new Thread(() -> {
                                try {
                                    Robot సింక్ = new Robot();
                                    సింక్.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception దోషం) {
                                    throw new RuntimeException(దోషం);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception దోషం) {
                throw new RuntimeException(దోషం);
            }
        }
    }

    public static void main(String[] 인수) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            విండో = new JFrame("QEMU 키보드·마우스 시험");
            JButton బటన్ = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            బటన్.addActionListener(ఈవెంట్ -> { 누름 = true; సరిచూడు(); });
            విండో.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            విండో.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent ఈవెంట్) { 키입력 = true; సరిచూడు(); }
            });
            విండో.add(బటన్);
            విండో.setSize(600, 180);
            విండో.setLocation(120, 120);
            విండో.setAlwaysOnTop(true);
            విండో.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            విండో.setVisible(true);
            విండో.toFront();
            Timer సిద్ధం_చేయు = new Timer(750, ఈవెంట్ -> {
                Point స్థానము = బటన్.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (స్థానము.x + బటన్.getWidth() / 2)
                        + " " + (స్థానము.y + బటన్.getHeight() / 2));
            });
            సిద్ధం_చేయు.setRepeats(false);
            సిద్ధం_చేయు.start();
        });
    }
}
