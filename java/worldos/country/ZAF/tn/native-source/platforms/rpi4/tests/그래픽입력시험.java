// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame fensetere;

    private static void netefatsa() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            fensetere.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window setotwa : Window.getWindows()) {
                        if (setotwa instanceof JFrame && setotwa.isVisible()
                                && ((JFrame) setotwa).getTitle().equals("다국어 인사")) {
                            setotwa.toFront();
                            new Thread(() -> {
                                try {
                                    Robot tsamaisanya = new Robot();
                                    tsamaisanya.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception phoso) {
                                    throw new RuntimeException(phoso);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception phoso) {
                throw new RuntimeException(phoso);
            }
        }
    }

    public static void main(String[] 인수) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            fensetere = new JFrame("QEMU 키보드·마우스 시험");
            JButton konopo = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            konopo.addActionListener(tiragalo -> { 누름 = true; netefatsa(); });
            fensetere.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            fensetere.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent tiragalo) { 키입력 = true; netefatsa(); }
            });
            fensetere.add(konopo);
            fensetere.setSize(600, 180);
            fensetere.setLocation(120, 120);
            fensetere.setAlwaysOnTop(true);
            fensetere.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            fensetere.setVisible(true);
            fensetere.toFront();
            Timer Baakanya = new Timer(750, tiragalo -> {
                Point 위치 = konopo.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (위치.x + konopo.getWidth() / 2)
                        + " " + (위치.y + konopo.getHeight() / 2));
            });
            Baakanya.setRepeats(false);
            Baakanya.start();
        });
    }
}
