// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class графика_входные_данные_тест {
    private static boolean Ключ_входные_данные, 누름;
    private static JFrame Окно;

    private static void проверять() {
        if (Ключ_входные_данные && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            Окно.dispose();
            try {
                Class.forName("приветствие_ae353e94").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window целевое_значение : Window.getWindows()) {
                        if (целевое_значение instanceof JFrame && целевое_значение.isVisible()
                                && ((JFrame) целевое_значение).getTitle().equals("다국어 приветствие_ae353e94")) {
                            целевое_значение.toFront();
                            new Thread(() -> {
                                try {
                                    Robot синхронизировать = new Robot();
                                    синхронизировать.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception ошибка) {
                                    throw new RuntimeException(ошибка);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("приветствие_ae353e94 창이 표시되지 않았습니다");
                });
            } catch (Exception ошибка) {
                throw new RuntimeException(ошибка);
            }
        }
    }

    public static void main(String[] аргументы) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 экран 없음");
        SwingUtilities.invokeAndWait(() -> {
            Окно = new JFrame("QEMU 키보드·마우스 испытания");
            JButton кнопка = new JButton("한글 экран · 이 단추를 누르고 K를 входные_данные_ЗНАЧЕН");
            кнопка.addActionListener(Событие -> { 누름 = true; проверять(); });
            Окно.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            Окно.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent Событие) { Ключ_входные_данные = true; проверять(); }
            });
            Окно.add(кнопка);
            Окно.setSize(600, 180);
            Окно.setLocation(120, 120);
            Окно.setAlwaysOnTop(true);
            Окно.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            Окно.setVisible(true);
            Окно.toFront();
            Timer Подготовить = new Timer(750, Событие -> {
                Point позиция = кнопка.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (позиция.x + кнопка.getWidth() / 2)
                        + " " + (позиция.y + кнопка.getHeight() / 2));
            });
            Подготовить.setRepeats(false);
            Подготовить.start();
        });
    }
}
