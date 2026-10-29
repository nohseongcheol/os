// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame цонх;

    private static void шалгах() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            цонх.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window зорилго : Window.getWindows()) {
                        if (зорилго instanceof JFrame && зорилго.isVisible()
                                && ((JFrame) зорилго).getTitle().equals("다국어 인사")) {
                            зорилго.toFront();
                            new Thread(() -> {
                                try {
                                    Robot синхрончлох = new Robot();
                                    синхрончлох.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception Алдаа) {
                                    throw new RuntimeException(Алдаа);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception Алдаа) {
                throw new RuntimeException(Алдаа);
            }
        }
    }

    public static void main(String[] 인수) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            цонх = new JFrame("QEMU 키보드·마우스 시험");
            JButton товч = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            товч.addActionListener(үйлдэл -> { 누름 = true; шалгах(); });
            цонх.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            цонх.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent үйлдэл) { 키입력 = true; шалгах(); }
            });
            цонх.add(товч);
            цонх.setSize(600, 180);
            цонх.setLocation(120, 120);
            цонх.setAlwaysOnTop(true);
            цонх.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            цонх.setVisible(true);
            цонх.toFront();
            Timer Бэлтгэх = new Timer(750, үйлдэл -> {
                Point 위치 = товч.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (위치.x + товч.getWidth() / 2)
                        + " " + (위치.y + товч.getHeight() / 2));
            });
            Бэлтгэх.setRepeats(false);
            Бэлтгэх.start();
        });
    }
}
