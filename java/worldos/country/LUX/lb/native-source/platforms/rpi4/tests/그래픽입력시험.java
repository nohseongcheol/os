// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame Fënster;

    private static void verifizéieren() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            Fënster.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window Zil : Window.getWindows()) {
                        if (Zil instanceof JFrame && Zil.isVisible()
                                && ((JFrame) Zil).getTitle().equals("다국어 인사")) {
                            Zil.toFront();
                            new Thread(() -> {
                                try {
                                    Robot synchroniséieren = new Robot();
                                    synchroniséieren.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception Feeler) {
                                    throw new RuntimeException(Feeler);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception Feeler) {
                throw new RuntimeException(Feeler);
            }
        }
    }

    public static void main(String[] 인수) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            Fënster = new JFrame("QEMU 키보드·마우스 시험");
            JButton Tast = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            Tast.addActionListener(Evenement -> { 누름 = true; verifizéieren(); });
            Fënster.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            Fënster.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent Evenement) { 키입력 = true; verifizéieren(); }
            });
            Fënster.add(Tast);
            Fënster.setSize(600, 180);
            Fënster.setLocation(120, 120);
            Fënster.setAlwaysOnTop(true);
            Fënster.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            Fënster.setVisible(true);
            Fënster.toFront();
            Timer Préparéieren = new Timer(750, Evenement -> {
                Point positionéieren = Tast.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (positionéieren.x + Tast.getWidth() / 2)
                        + " " + (positionéieren.y + Tast.getHeight() / 2));
            });
            Préparéieren.setRepeats(false);
            Préparéieren.start();
        });
    }
}
