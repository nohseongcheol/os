// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, 누름;
    private static JFrame ifasitela;

    private static void qiniseka() {
        if (키입력 && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            ifasitela.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window impokophelo : Window.getWindows()) {
                        if (impokophelo instanceof JFrame && impokophelo.isVisible()
                                && ((JFrame) impokophelo).getTitle().equals("다국어 인사")) {
                            impokophelo.toFront();
                            new Thread(() -> {
                                try {
                                    Robot i_sync = new Robot();
                                    i_sync.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception Iphutha) {
                                    throw new RuntimeException(Iphutha);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception Iphutha) {
                throw new RuntimeException(Iphutha);
            }
        }
    }

    public static void main(String[] 인수) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            ifasitela = new JFrame("QEMU 키보드·마우스 시험");
            JButton inkinobho = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            inkinobho.addActionListener(isigameko -> { 누름 = true; qiniseka(); });
            ifasitela.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            ifasitela.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent isigameko) { 키입력 = true; qiniseka(); }
            });
            ifasitela.add(inkinobho);
            ifasitela.setSize(600, 180);
            ifasitela.setLocation(120, 120);
            ifasitela.setAlwaysOnTop(true);
            ifasitela.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            ifasitela.setVisible(true);
            ifasitela.toFront();
            Timer Hlela = new Timer(750, isigameko -> {
                Point 위치 = inkinobho.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (위치.x + inkinobho.getWidth() / 2)
                        + " " + (위치.y + inkinobho.getHeight() / 2));
            });
            Hlela.setRepeats(false);
            Hlela.start();
        });
    }
}
