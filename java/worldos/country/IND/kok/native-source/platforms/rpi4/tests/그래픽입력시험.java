// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame विंडो;

    private static void पुनर्तपासणी_करची() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            विंडो.dispose();
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
                                    Robot सिंक्रोनायझ = new Robot();
                                    सिंक्रोनायझ.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception चूक) {
                                    throw new RuntimeException(चूक);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception चूक) {
                throw new RuntimeException(चूक);
            }
        }
    }

    public static void main(String[] 인수) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            विंडो = new JFrame("QEMU 키보드·마우스 시험");
            JButton बटन = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            बटन.addActionListener(प्रसंग -> { 누름 = true; पुनर्तपासणी_करची(); });
            विंडो.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            विंडो.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent प्रसंग) { 키입력 = true; पुनर्तपासणी_करची(); }
            });
            विंडो.add(बटन);
            विंडो.setSize(600, 180);
            विंडो.setLocation(120, 120);
            विंडो.setAlwaysOnTop(true);
            विंडो.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            विंडो.setVisible(true);
            विंडो.toFront();
            Timer तयार_करचें_9ce364fc = new Timer(750, प्रसंग -> {
                Point स्थिती = बटन.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (स्थिती.x + बटन.getWidth() / 2)
                        + " " + (स्थिती.y + बटन.getHeight() / 2));
            });
            तयार_करचें_9ce364fc.setRepeats(false);
            तयार_करचें_9ce364fc.start();
        });
    }
}
