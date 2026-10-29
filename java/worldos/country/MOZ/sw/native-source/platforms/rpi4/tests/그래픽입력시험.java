// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame dirisha;

    private static void thibitisha() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            dirisha.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window lengo : Window.getWindows()) {
                        if (lengo instanceof JFrame && lengo.isVisible()
                                && ((JFrame) lengo).getTitle().equals("다국어 인사")) {
                            lengo.toFront();
                            new Thread(() -> {
                                try {
                                    Robot landanisha = new Robot();
                                    landanisha.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception kosa) {
                                    throw new RuntimeException(kosa);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception kosa) {
                throw new RuntimeException(kosa);
            }
        }
    }

    public static void main(String[] 인수) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            dirisha = new JFrame("QEMU 키보드·마우스 시험");
            JButton kitufe = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            kitufe.addActionListener(tukio -> { 누름 = true; thibitisha(); });
            dirisha.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            dirisha.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent tukio) { 키입력 = true; thibitisha(); }
            });
            dirisha.add(kitufe);
            dirisha.setSize(600, 180);
            dirisha.setLocation(120, 120);
            dirisha.setAlwaysOnTop(true);
            dirisha.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            dirisha.setVisible(true);
            dirisha.toFront();
            Timer Andaa = new Timer(750, tukio -> {
                Point 위치 = kitufe.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (위치.x + kitufe.getWidth() / 2)
                        + " " + (위치.y + kitufe.getHeight() / 2));
            });
            Andaa.setRepeats(false);
            Andaa.start();
        });
    }
}
