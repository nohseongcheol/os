// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame fuinneog;

    private static void fíoraigh() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            fuinneog.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window sprioc : Window.getWindows()) {
                        if (sprioc instanceof JFrame && sprioc.isVisible()
                                && ((JFrame) sprioc).getTitle().equals("다국어 인사")) {
                            sprioc.toFront();
                            new Thread(() -> {
                                try {
                                    Robot sioncronaigh = new Robot();
                                    sioncronaigh.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception ERREÁID) {
                                    throw new RuntimeException(ERREÁID);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception ERREÁID) {
                throw new RuntimeException(ERREÁID);
            }
        }
    }

    public static void main(String[] Argóintí) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            fuinneog = new JFrame("QEMU 키보드·마우스 시험");
            JButton cnaipe = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            cnaipe.addActionListener(ócáid -> { 누름 = true; fíoraigh(); });
            fuinneog.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            fuinneog.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent ócáid) { 키입력 = true; fíoraigh(); }
            });
            fuinneog.add(cnaipe);
            fuinneog.setSize(600, 180);
            fuinneog.setLocation(120, 120);
            fuinneog.setAlwaysOnTop(true);
            fuinneog.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            fuinneog.setVisible(true);
            fuinneog.toFront();
            Timer Ullmhaigh = new Timer(750, ócáid -> {
                Point suíomh = cnaipe.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (suíomh.x + cnaipe.getWidth() / 2)
                        + " " + (suíomh.y + cnaipe.getHeight() / 2));
            });
            Ullmhaigh.setRepeats(false);
            Ullmhaigh.start();
        });
    }
}
