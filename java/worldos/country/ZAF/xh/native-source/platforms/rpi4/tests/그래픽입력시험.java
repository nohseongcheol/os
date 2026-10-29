// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame i_window;

    private static void ngqinisisa() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            i_window.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window ithagethi : Window.getWindows()) {
                        if (ithagethi instanceof JFrame && ithagethi.isVisible()
                                && ((JFrame) ithagethi).getTitle().equals("다국어 인사")) {
                            ithagethi.toFront();
                            new Thread(() -> {
                                try {
                                    Robot ngqamanisa = new Robot();
                                    ngqamanisa.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception Impazamo) {
                                    throw new RuntimeException(Impazamo);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception Impazamo) {
                throw new RuntimeException(Impazamo);
            }
        }
    }

    public static void main(String[] 인수) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            i_window = new JFrame("QEMU 키보드·마우스 시험");
            JButton iqhosha = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            iqhosha.addActionListener(umcimbi -> { 누름 = true; ngqinisisa(); });
            i_window.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            i_window.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent umcimbi) { 키입력 = true; ngqinisisa(); }
            });
            i_window.add(iqhosha);
            i_window.setSize(600, 180);
            i_window.setLocation(120, 120);
            i_window.setAlwaysOnTop(true);
            i_window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            i_window.setVisible(true);
            i_window.toFront();
            Timer lungisa = new Timer(750, umcimbi -> {
                Point 위치 = iqhosha.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (위치.x + iqhosha.getWidth() / 2)
                        + " " + (위치.y + iqhosha.getHeight() / 2));
            });
            lungisa.setRepeats(false);
            lungisa.start();
        });
    }
}
