// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame சாளரம்;

    private static void சரிபார்() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            சாளரம்.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window இலக்கு : Window.getWindows()) {
                        if (இலக்கு instanceof JFrame && இலக்கு.isVisible()
                                && ((JFrame) இலக்கு).getTitle().equals("다국어 인사")) {
                            இலக்கு.toFront();
                            new Thread(() -> {
                                try {
                                    Robot ஒத்திசை = new Robot();
                                    ஒத்திசை.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception பிழை) {
                                    throw new RuntimeException(பிழை);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception பிழை) {
                throw new RuntimeException(பிழை);
            }
        }
    }

    public static void main(String[] செயலுருபுகள்) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            சாளரம் = new JFrame("QEMU 키보드·마우스 시험");
            JButton பொத்தான் = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            பொத்தான்.addActionListener(நிகழ்வு -> { 누름 = true; சரிபார்(); });
            சாளரம்.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            சாளரம்.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent நிகழ்வு) { 키입력 = true; சரிபார்(); }
            });
            சாளரம்.add(பொத்தான்);
            சாளரம்.setSize(600, 180);
            சாளரம்.setLocation(120, 120);
            சாளரம்.setAlwaysOnTop(true);
            சாளரம்.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            சாளரம்.setVisible(true);
            சாளரம்.toFront();
            Timer தயார்படுத்த = new Timer(750, நிகழ்வு -> {
                Point இடம் = பொத்தான்.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (இடம்.x + பொத்தான்.getWidth() / 2)
                        + " " + (இடம்.y + பொத்தான்.getHeight() / 2));
            });
            தயார்படுத்த.setRepeats(false);
            தயார்படுத்த.start();
        });
    }
}
