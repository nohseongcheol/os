// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame falanteere;

    private static void ƴeewtaade() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            falanteere.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window faandaare : Window.getWindows()) {
                        if (faandaare instanceof JFrame && faandaare.isVisible()
                                && ((JFrame) faandaare).getTitle().equals("다국어 인사")) {
                            faandaare.toFront();
                            new Thread(() -> {
                                try {
                                    Robot sanngoɗinde = new Robot();
                                    sanngoɗinde.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception juumre) {
                                    throw new RuntimeException(juumre);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception juumre) {
                throw new RuntimeException(juumre);
            }
        }
    }

    public static void main(String[] 인수) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            falanteere = new JFrame("QEMU 키보드·마우스 시험");
            JButton feɗoode = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            feɗoode.addActionListener(saɗteende -> { 누름 = true; ƴeewtaade(); });
            falanteere.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            falanteere.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent saɗteende) { 키입력 = true; ƴeewtaade(); }
            });
            falanteere.add(feɗoode);
            falanteere.setSize(600, 180);
            falanteere.setLocation(120, 120);
            falanteere.setAlwaysOnTop(true);
            falanteere.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            falanteere.setVisible(true);
            falanteere.toFront();
            Timer Heblu = new Timer(750, saɗteende -> {
                Point 위치 = feɗoode.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (위치.x + feɗoode.getWidth() / 2)
                        + " " + (위치.y + feɗoode.getHeight() / 2));
            });
            Heblu.setRepeats(false);
            Heblu.start();
        });
    }
}
