// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, басу_мән_3efd25d6;
    private static JFrame Терезе;

    private static void тексеру() {
        if (키입력 && басу_мән_3efd25d6) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            Терезе.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window мақсатты_мән : Window.getWindows()) {
                        if (мақсатты_мән instanceof JFrame && мақсатты_мән.isVisible()
                                && ((JFrame) мақсатты_мән).getTitle().equals("다국어 인사")) {
                            мақсатты_мән.toFront();
                            new Thread(() -> {
                                try {
                                    Robot үндестіру = new Robot();
                                    үндестіру.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception Қате) {
                                    throw new RuntimeException(Қате);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception Қате) {
                throw new RuntimeException(Қате);
            }
        }
    }

    public static void main(String[] Аргументтер) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            Терезе = new JFrame("QEMU 키보드·마우스 시험");
            JButton батырма = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            батырма.addActionListener(Оқиға -> { басу_мән_3efd25d6 = true; тексеру(); });
            Терезе.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            Терезе.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent Оқиға) { 키입력 = true; тексеру(); }
            });
            Терезе.add(батырма);
            Терезе.setSize(600, 180);
            Терезе.setLocation(120, 120);
            Терезе.setAlwaysOnTop(true);
            Терезе.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            Терезе.setVisible(true);
            Терезе.toFront();
            Timer Дайындау = new Timer(750, Оқиға -> {
                Point Орны = батырма.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (Орны.x + батырма.getWidth() / 2)
                        + " " + (Орны.y + батырма.getHeight() / 2));
            });
            Дайындау.setRepeats(false);
            Дайындау.start();
        });
    }
}
