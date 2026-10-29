// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame सन्झ्याल;

    private static void रुजू_गर्नुहोस्() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            सन्झ्याल.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window लक्ष्य : Window.getWindows()) {
                        if (लक्ष्य instanceof JFrame && लक्ष्य.isVisible()
                                && ((JFrame) लक्ष्य).getTitle().equals("다국어 인사")) {
                            लक्ष्य.toFront();
                            new Thread(() -> {
                                try {
                                    Robot समक्रमित = new Robot();
                                    समक्रमित.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception त्रुटि) {
                                    throw new RuntimeException(त्रुटि);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception त्रुटि) {
                throw new RuntimeException(त्रुटि);
            }
        }
    }

    public static void main(String[] तर्क) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            सन्झ्याल = new JFrame("QEMU 키보드·마우스 시험");
            JButton बटन = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            बटन.addActionListener(घटना -> { 누름 = true; रुजू_गर्नुहोस्(); });
            सन्झ्याल.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            सन्झ्याल.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent घटना) { 키입력 = true; रुजू_गर्नुहोस्(); }
            });
            सन्झ्याल.add(बटन);
            सन्झ्याल.setSize(600, 180);
            सन्झ्याल.setLocation(120, 120);
            सन्झ्याल.setAlwaysOnTop(true);
            सन्झ्याल.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            सन्झ्याल.setVisible(true);
            सन्झ्याल.toFront();
            Timer तयार_गर्नुहोस् = new Timer(750, घटना -> {
                Point स्थिति = बटन.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (स्थिति.x + बटन.getWidth() / 2)
                        + " " + (स्थिति.y + बटन.getHeight() / 2));
            });
            तयार_गर्नुहोस्.setRepeats(false);
            तयार_गर्नुहोस्.start();
        });
    }
}
