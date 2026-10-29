// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, pritisnuti_VALUE;
    private static JFrame prozor;

    private static void potvrditi() {
        if (키입력 && pritisnuti_VALUE) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            prozor.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window cilj : Window.getWindows()) {
                        if (cilj instanceof JFrame && cilj.isVisible()
                                && ((JFrame) cilj).getTitle().equals("다국어 인사")) {
                            cilj.toFront();
                            new Thread(() -> {
                                try {
                                    Robot sinhronizirati = new Robot();
                                    sinhronizirati.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception GRESKA) {
                                    throw new RuntimeException(GRESKA);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception GRESKA) {
                throw new RuntimeException(GRESKA);
            }
        }
    }

    public static void main(String[] Argumenti) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            prozor = new JFrame("QEMU 키보드·마우스 시험");
            JButton dugme = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            dugme.addActionListener(događaj -> { pritisnuti_VALUE = true; potvrditi(); });
            prozor.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            prozor.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent događaj) { 키입력 = true; potvrditi(); }
            });
            prozor.add(dugme);
            prozor.setSize(600, 180);
            prozor.setLocation(120, 120);
            prozor.setAlwaysOnTop(true);
            prozor.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            prozor.setVisible(true);
            prozor.toFront();
            Timer Pripremiti = new Timer(750, događaj -> {
                Point Pozicija = dugme.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (Pozicija.x + dugme.getWidth() / 2)
                        + " " + (Pozicija.y + dugme.getHeight() / 2));
            });
            Pripremiti.setRepeats(false);
            Pripremiti.start();
        });
    }
}
