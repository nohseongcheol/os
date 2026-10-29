// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, натиснути_значення;
    private static JFrame Вікно;

    private static void перевіряти() {
        if (키입력 && натиснути_значення) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            Вікно.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window мета : Window.getWindows()) {
                        if (мета instanceof JFrame && мета.isVisible()
                                && ((JFrame) мета).getTitle().equals("다국어 인사")) {
                            мета.toFront();
                            new Thread(() -> {
                                try {
                                    Robot синхронізувати = new Robot();
                                    синхронізувати.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception ПОМИЛКА) {
                                    throw new RuntimeException(ПОМИЛКА);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception ПОМИЛКА) {
                throw new RuntimeException(ПОМИЛКА);
            }
        }
    }

    public static void main(String[] аргументи) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            Вікно = new JFrame("QEMU 키보드·마우스 випробування");
            JButton кнопка = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            кнопка.addActionListener(Подія -> { натиснути_значення = true; перевіряти(); });
            Вікно.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            Вікно.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent Подія) { 키입력 = true; перевіряти(); }
            });
            Вікно.add(кнопка);
            Вікно.setSize(600, 180);
            Вікно.setLocation(120, 120);
            Вікно.setAlwaysOnTop(true);
            Вікно.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            Вікно.setVisible(true);
            Вікно.toFront();
            Timer Готувати = new Timer(750, Подія -> {
                Point позиція = кнопка.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (позиція.x + кнопка.getWidth() / 2)
                        + " " + (позиція.y + кнопка.getHeight() / 2));
            });
            Готувати.setRepeats(false);
            Готувати.start();
        });
    }
}
