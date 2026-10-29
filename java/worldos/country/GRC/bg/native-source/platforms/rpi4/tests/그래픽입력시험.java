// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, натискам_стойност;
    private static JFrame Прозорец;

    private static void проверявам() {
        if (키입력 && натискам_стойност) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            Прозорец.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window цел : Window.getWindows()) {
                        if (цел instanceof JFrame && цел.isVisible()
                                && ((JFrame) цел).getTitle().equals("다국어 인사")) {
                            цел.toFront();
                            new Thread(() -> {
                                try {
                                    Robot синхронизирам = new Robot();
                                    синхронизирам.waitForIdle();
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

    public static void main(String[] Параметри) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            Прозорец = new JFrame("QEMU 키보드·마우스 시험");
            JButton бутон = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            бутон.addActionListener(Събитие -> { натискам_стойност = true; проверявам(); });
            Прозорец.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            Прозорец.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent Събитие) { 키입력 = true; проверявам(); }
            });
            Прозорец.add(бутон);
            Прозорец.setSize(600, 180);
            Прозорец.setLocation(120, 120);
            Прозорец.setAlwaysOnTop(true);
            Прозорец.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            Прозорец.setVisible(true);
            Прозорец.toFront();
            Timer Подготвяне = new Timer(750, Събитие -> {
                Point Позиция = бутон.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (Позиция.x + бутон.getWidth() / 2)
                        + " " + (Позиция.y + бутон.getHeight() / 2));
            });
            Подготвяне.setRepeats(false);
            Подготвяне.start();
        });
    }
}
