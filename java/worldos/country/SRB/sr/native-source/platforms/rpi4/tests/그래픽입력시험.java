// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame Прозор;

    private static void 확인() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            Прозор.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window 대상 : Window.getWindows()) {
                        if (대상 instanceof JFrame && 대상.isVisible()
                                && ((JFrame) 대상).getTitle().equals("다국어 인사")) {
                            대상.toFront();
                            new Thread(() -> {
                                try {
                                    Robot 동기화 = new Robot();
                                    동기화.waitForIdle();
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
            дугме.addActionListener(Догађај -> { 누름 = true; 확인(); });
            Прозор.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            Прозор.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent Догађај) { 키입력 = true; 확인(); }
            });
            Прозор.add(дугме);
            Прозор.setSize(600, 180);
            Прозор.setLocation(120, 120);
            Прозор.setAlwaysOnTop(true);
            Прозор.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            Прозор.setVisible(true);
            Прозор.toFront();
            Timer 준비 = new Timer(750, Догађај -> {
                Point Положај = дугме.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (Положај.x + дугме.getWidth() / 2)
                        + " " + (Положај.y + дугме.getHeight() / 2));
            });
            준비.setRepeats(false);
            준비.start();
        });
    }
}
