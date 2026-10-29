// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame прозор;

    private static void потврдити() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            прозор.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window циљ : Window.getWindows()) {
                        if (циљ instanceof JFrame && циљ.isVisible()
                                && ((JFrame) циљ).getTitle().equals("다국어 인사")) {
                            циљ.toFront();
                            new Thread(() -> {
                                try {
                                    Robot синхронизирати = new Robot();
                                    синхронизирати.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception грешка) {
                                    throw new RuntimeException(грешка);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception грешка) {
                throw new RuntimeException(грешка);
            }
        }
    }

    public static void main(String[] 인수) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            прозор = new JFrame("QEMU 키보드·마우스 시험");
            JButton дугме = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            дугме.addActionListener(догађај -> { 누름 = true; потврдити(); });
            прозор.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            прозор.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent догађај) { 키입력 = true; потврдити(); }
            });
            прозор.add(дугме);
            прозор.setSize(600, 180);
            прозор.setLocation(120, 120);
            прозор.setAlwaysOnTop(true);
            прозор.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            прозор.setVisible(true);
            прозор.toFront();
            Timer Припремити = new Timer(750, догађај -> {
                Point 위치 = дугме.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (위치.x + дугме.getWidth() / 2)
                        + " " + (위치.y + дугме.getHeight() / 2));
            });
            Припремити.setRepeats(false);
            Припремити.start();
        });
    }
}
