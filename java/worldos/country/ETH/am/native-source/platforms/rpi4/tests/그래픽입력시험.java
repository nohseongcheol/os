// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame መስኮት;

    private static void አረጋግጥ() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            መስኮት.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window ዓላማ : Window.getWindows()) {
                        if (ዓላማ instanceof JFrame && ዓላማ.isVisible()
                                && ((JFrame) ዓላማ).getTitle().equals("다국어 인사")) {
                            ዓላማ.toFront();
                            new Thread(() -> {
                                try {
                                    Robot አመሳስል = new Robot();
                                    አመሳስል.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception ስህተት) {
                                    throw new RuntimeException(ስህተት);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception ስህተት) {
                throw new RuntimeException(ስህተት);
            }
        }
    }

    public static void main(String[] 인수) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            መስኮት = new JFrame("QEMU 키보드·마우스 시험");
            JButton አዝራር = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            አዝራር.addActionListener(ፍጻሜ -> { 누름 = true; አረጋግጥ(); });
            መስኮት.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            መስኮት.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent ፍጻሜ) { 키입력 = true; አረጋግጥ(); }
            });
            መስኮት.add(አዝራር);
            መስኮት.setSize(600, 180);
            መስኮት.setLocation(120, 120);
            መስኮት.setAlwaysOnTop(true);
            መስኮት.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            መስኮት.setVisible(true);
            መስኮት.toFront();
            Timer አዘጋጅ_9ce364fc = new Timer(750, ፍጻሜ -> {
                Point አካባቢ = አዝራር.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (አካባቢ.x + አዝራር.getWidth() / 2)
                        + " " + (አካባቢ.y + አዝራር.getHeight() / 2));
            });
            አዘጋጅ_9ce364fc.setRepeats(false);
            አዘጋጅ_9ce364fc.start();
        });
    }
}
