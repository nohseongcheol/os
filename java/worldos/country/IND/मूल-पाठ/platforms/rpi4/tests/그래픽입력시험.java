// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, दबाएँ_मान;
    private static JFrame खिड़की;

    private static void सत्यापित_करें() {
        if (키입력 && दबाएँ_मान) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            खिड़की.dispose();
            try {
                Class.forName("अभिनन्दन_ae353e94").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window लक्ष्य : Window.getWindows()) {
                        if (लक्ष्य instanceof JFrame && लक्ष्य.isVisible()
                                && ((JFrame) लक्ष्य).getTitle().equals("다국어 अभिनन्दन_ae353e94")) {
                            लक्ष्य.toFront();
                            new Thread(() -> {
                                try {
                                    Robot सिंक्रनाइज़_करें = new Robot();
                                    सिंक्रनाइज़_करें.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception त्रुटि) {
                                    throw new RuntimeException(त्रुटि);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("अभिनन्दन_ae353e94 창이 표시되지 않았습니다");
                });
            } catch (Exception त्रुटि) {
                throw new RuntimeException(त्रुटि);
            }
        }
    }

    public static void main(String[] तर्क) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            खिड़की = new JFrame("QEMU 키보드·마우스 시험");
            JButton बटन = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            बटन.addActionListener(घटना -> { दबाएँ_मान = true; सत्यापित_करें(); });
            खिड़की.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            खिड़की.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent घटना) { 키입력 = true; सत्यापित_करें(); }
            });
            खिड़की.add(बटन);
            खिड़की.setSize(600, 180);
            खिड़की.setLocation(120, 120);
            खिड़की.setAlwaysOnTop(true);
            खिड़की.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            खिड़की.setVisible(true);
            खिड़की.toFront();
            Timer 준비 = new Timer(750, घटना -> {
                Point स्थान = बटन.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (स्थान.x + बटन.getWidth() / 2)
                        + " " + (स्थान.y + बटन.getHeight() / 2));
            });
            준비.setRepeats(false);
            준비.start();
        });
    }
}
