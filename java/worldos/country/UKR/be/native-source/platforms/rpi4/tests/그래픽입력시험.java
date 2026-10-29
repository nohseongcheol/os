// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame акно;

    private static void праверыць() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            акно.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window мэтавы_паказчык : Window.getWindows()) {
                        if (мэтавы_паказчык instanceof JFrame && мэтавы_паказчык.isVisible()
                                && ((JFrame) мэтавы_паказчык).getTitle().equals("다국어 인사")) {
                            мэтавы_паказчык.toFront();
                            new Thread(() -> {
                                try {
                                    Robot сінхранізаваць = new Robot();
                                    сінхранізаваць.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception ПАМЫЛКА) {
                                    throw new RuntimeException(ПАМЫЛКА);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception ПАМЫЛКА) {
                throw new RuntimeException(ПАМЫЛКА);
            }
        }
    }

    public static void main(String[] 인수) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            акно = new JFrame("QEMU 키보드·마우스 시험");
            JButton кнопка = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            кнопка.addActionListener(Падзея -> { 누름 = true; праверыць(); });
            акно.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            акно.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent Падзея) { 키입력 = true; праверыць(); }
            });
            акно.add(кнопка);
            акно.setSize(600, 180);
            акно.setLocation(120, 120);
            акно.setAlwaysOnTop(true);
            акно.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            акно.setVisible(true);
            акно.toFront();
            Timer Падрыхтаваць = new Timer(750, Падзея -> {
                Point Пазіцыя = кнопка.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (Пазіцыя.x + кнопка.getWidth() / 2)
                        + " " + (Пазіцыя.y + кнопка.getHeight() / 2));
            });
            Падрыхтаваць.setRepeats(false);
            Падрыхтаваць.start();
        });
    }
}
