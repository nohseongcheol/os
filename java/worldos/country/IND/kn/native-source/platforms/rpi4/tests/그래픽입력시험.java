// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame ವಿಂಡೋ;

    private static void ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            ವಿಂಡೋ.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window ಲಕ್ಷ್ಯ : Window.getWindows()) {
                        if (ಲಕ್ಷ್ಯ instanceof JFrame && ಲಕ್ಷ್ಯ.isVisible()
                                && ((JFrame) ಲಕ್ಷ್ಯ).getTitle().equals("다국어 인사")) {
                            ಲಕ್ಷ್ಯ.toFront();
                            new Thread(() -> {
                                try {
                                    Robot ಸಿಂಕ್_ಮಾಡು = new Robot();
                                    ಸಿಂಕ್_ಮಾಡು.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception ದೋಷ) {
                                    throw new RuntimeException(ದೋಷ);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception ದೋಷ) {
                throw new RuntimeException(ದೋಷ);
            }
        }
    }

    public static void main(String[] 인수) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            ವಿಂಡೋ = new JFrame("QEMU 키보드·마우스 시험");
            JButton ಬಟನ್ = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            ಬಟನ್.addActionListener(ಸಂಗತಿ -> { 누름 = true; ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(); });
            ವಿಂಡೋ.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            ವಿಂಡೋ.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent ಸಂಗತಿ) { 키입력 = true; ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು(); }
            });
            ವಿಂಡೋ.add(ಬಟನ್);
            ವಿಂಡೋ.setSize(600, 180);
            ವಿಂಡೋ.setLocation(120, 120);
            ವಿಂಡೋ.setAlwaysOnTop(true);
            ವಿಂಡೋ.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            ವಿಂಡೋ.setVisible(true);
            ವಿಂಡೋ.toFront();
            Timer ಸಿದ್ಧಪಡಿಸು = new Timer(750, ಸಂಗತಿ -> {
                Point ಸ್ಥಾನ = ಬಟನ್.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (ಸ್ಥಾನ.x + ಬಟನ್.getWidth() / 2)
                        + " " + (ಸ್ಥಾನ.y + ಬಟನ್.getHeight() / 2));
            });
            ಸಿದ್ಧಪಡಿಸು.setRepeats(false);
            ಸಿದ್ಧಪಡಿಸು.start();
        });
    }
}
