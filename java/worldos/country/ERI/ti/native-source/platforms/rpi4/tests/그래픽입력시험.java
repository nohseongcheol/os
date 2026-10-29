// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame መስኮት;

    private static void ኣረጋግጽ() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            መስኮት.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window ዕላማ : Window.getWindows()) {
                        if (ዕላማ instanceof JFrame && ዕላማ.isVisible()
                                && ((JFrame) ዕላማ).getTitle().equals("다국어 인사")) {
                            ዕላማ.toFront();
                            new Thread(() -> {
                                try {
                                    Robot ኣሳንይ = new Robot();
                                    ኣሳንይ.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception ጌጋ) {
                                    throw new RuntimeException(ጌጋ);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception ጌጋ) {
                throw new RuntimeException(ጌጋ);
            }
        }
    }

    public static void main(String[] 인수) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            መስኮት = new JFrame("QEMU 키보드·마우스 시험");
            JButton መጠወቒ = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            መጠወቒ.addActionListener(ፍጻመ -> { 누름 = true; ኣረጋግጽ(); });
            መስኮት.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            መስኮት.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent ፍጻመ) { 키입력 = true; ኣረጋግጽ(); }
            });
            መስኮት.add(መጠወቒ);
            መስኮት.setSize(600, 180);
            መስኮት.setLocation(120, 120);
            መስኮት.setAlwaysOnTop(true);
            መስኮት.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            መስኮት.setVisible(true);
            መስኮት.toFront();
            Timer ኣዳልው = new Timer(750, ፍጻመ -> {
                Point 위치 = መጠወቒ.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (위치.x + መጠወቒ.getWidth() / 2)
                        + " " + (위치.y + መጠወቒ.getHeight() / 2));
            });
            ኣዳልው.setRepeats(false);
            ኣዳልው.start();
        });
    }
}
