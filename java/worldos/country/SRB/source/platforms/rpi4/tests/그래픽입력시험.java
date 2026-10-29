// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, отиснути_вриједност;
    private static JFrame Прозор;

    private static void потврдити() {
        if (키입력 && отиснути_вриједност) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            Прозор.dispose();
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
                                } catch (Exception ГРЕШКА) {
                                    throw new RuntimeException(ГРЕШКА);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception ГРЕШКА) {
                throw new RuntimeException(ГРЕШКА);
            }
        }
    }

    public static void main(String[] Аргументи) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            Прозор = new JFrame("QEMU 키보드·마우스 시험");
            JButton дугме = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            дугме.addActionListener(Догађај -> { отиснути_вриједност = true; потврдити(); });
            Прозор.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            Прозор.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent Догађај) { 키입력 = true; потврдити(); }
            });
            Прозор.add(дугме);
            Прозор.setSize(600, 180);
            Прозор.setLocation(120, 120);
            Прозор.setAlwaysOnTop(true);
            Прозор.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            Прозор.setVisible(true);
            Прозор.toFront();
            Timer Припремити = new Timer(750, Догађај -> {
                Point Положај = дугме.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (Положај.x + дугме.getWidth() / 2)
                        + " " + (Положај.y + дугме.getHeight() / 2));
            });
            Припремити.setRepeats(false);
            Припремити.start();
        });
    }
}
