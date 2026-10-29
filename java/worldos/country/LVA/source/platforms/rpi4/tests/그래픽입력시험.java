// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, nospiest_VALUE;
    private static JFrame Logs;

    private static void verificēt() {
        if (키입력 && nospiest_VALUE) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            Logs.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window mērķis : Window.getWindows()) {
                        if (mērķis instanceof JFrame && mērķis.isVisible()
                                && ((JFrame) mērķis).getTitle().equals("다국어 인사")) {
                            mērķis.toFront();
                            new Thread(() -> {
                                try {
                                    Robot sinhronizēt = new Robot();
                                    sinhronizēt.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception Kļūda) {
                                    throw new RuntimeException(Kļūda);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception Kļūda) {
                throw new RuntimeException(Kļūda);
            }
        }
    }

    public static void main(String[] Parametri) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            Logs = new JFrame("QEMU 키보드·마우스 시험");
            JButton Pogas = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            Pogas.addActionListener(Notikums -> { nospiest_VALUE = true; verificēt(); });
            Logs.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            Logs.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent Notikums) { 키입력 = true; verificēt(); }
            });
            Logs.add(Pogas);
            Logs.setSize(600, 180);
            Logs.setLocation(120, 120);
            Logs.setAlwaysOnTop(true);
            Logs.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            Logs.setVisible(true);
            Logs.toFront();
            Timer Sagatavot = new Timer(750, Notikums -> {
                Point Novietojums = Pogas.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (Novietojums.x + Pogas.getWidth() / 2)
                        + " " + (Novietojums.y + Pogas.getHeight() / 2));
            });
            Sagatavot.setRepeats(false);
            Sagatavot.start();
        });
    }
}
