// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame كۆزنەك;

    private static void دەلىللىمەك() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            كۆزنەك.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window نىشان : Window.getWindows()) {
                        if (نىشان instanceof JFrame && نىشان.isVisible()
                                && ((JFrame) نىشان).getTitle().equals("다국어 인사")) {
                            نىشان.toFront();
                            new Thread(() -> {
                                try {
                                    Robot ماسقەدەملەش = new Robot();
                                    ماسقەدەملەش.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception خاتالىق) {
                                    throw new RuntimeException(خاتالىق);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception خاتالىق) {
                throw new RuntimeException(خاتالىق);
            }
        }
    }

    public static void main(String[] ئۆزگەرگۈچىلەر) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            كۆزنەك = new JFrame("QEMU 키보드·마우스 시험");
            JButton كۇنۇپكا = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            كۇنۇپكا.addActionListener(ھادىسە -> { 누름 = true; دەلىللىمەك(); });
            كۆزنەك.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            كۆزنەك.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent ھادىسە) { 키입력 = true; دەلىللىمەك(); }
            });
            كۆزنەك.add(كۇنۇپكا);
            كۆزنەك.setSize(600, 180);
            كۆزنەك.setLocation(120, 120);
            كۆزنەك.setAlwaysOnTop(true);
            كۆزنەك.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            كۆزنەك.setVisible(true);
            كۆزنەك.toFront();
            Timer تەييارلىماق = new Timer(750, ھادىسە -> {
                Point ئورۇن = كۇنۇپكا.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (ئورۇن.x + كۇنۇپكا.getWidth() / 2)
                        + " " + (ئورۇن.y + كۇنۇپكا.getHeight() / 2));
            });
            تەييارلىماق.setRepeats(false);
            تەييارلىماق.start();
        });
    }
}
