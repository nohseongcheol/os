// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, sakatu_balio;
    private static JFrame Leihoa;

    private static void egiaztatu() {
        if (키입력 && sakatu_balio) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            Leihoa.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window helburu_balio : Window.getWindows()) {
                        if (helburu_balio instanceof JFrame && helburu_balio.isVisible()
                                && ((JFrame) helburu_balio).getTitle().equals("다국어 인사")) {
                            helburu_balio.toFront();
                            new Thread(() -> {
                                try {
                                    Robot sinkronizatu = new Robot();
                                    sinkronizatu.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception errorea) {
                                    throw new RuntimeException(errorea);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception errorea) {
                throw new RuntimeException(errorea);
            }
        }
    }

    public static void main(String[] Argumentuak) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            Leihoa = new JFrame("QEMU 키보드·마우스 시험");
            JButton botoia = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            botoia.addActionListener(Gertaera -> { sakatu_balio = true; egiaztatu(); });
            Leihoa.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            Leihoa.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent Gertaera) { 키입력 = true; egiaztatu(); }
            });
            Leihoa.add(botoia);
            Leihoa.setSize(600, 180);
            Leihoa.setLocation(120, 120);
            Leihoa.setAlwaysOnTop(true);
            Leihoa.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            Leihoa.setVisible(true);
            Leihoa.toFront();
            Timer 준비 = new Timer(750, Gertaera -> {
                Point Posizioa = botoia.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (Posizioa.x + botoia.getWidth() / 2)
                        + " " + (Posizioa.y + botoia.getHeight() / 2));
            });
            준비.setRepeats(false);
            준비.start();
        });
    }
}
