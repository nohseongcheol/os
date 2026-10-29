// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class grafik_artış_test {
    private static boolean tuş_artış, bas_değer;
    private static JFrame Pencere;

    private static void doğrulamak() {
        if (tuş_artış && bas_değer) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            Pencere.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window hedef : Window.getWindows()) {
                        if (hedef instanceof JFrame && hedef.isVisible()
                                && ((JFrame) hedef).getTitle().equals("다국어 인사")) {
                            hedef.toFront();
                            new Thread(() -> {
                                try {
                                    Robot eşitlemek = new Robot();
                                    eşitlemek.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception hata) {
                                    throw new RuntimeException(hata);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception hata) {
                throw new RuntimeException(hata);
            }
        }
    }

    public static void main(String[] bağımsız_değişkenler) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            Pencere = new JFrame("QEMU 키보드·마우스 sınamalar");
            JButton düğme = new JButton("한글 화면 · 이 단추를 누르고 K를 artış_değer");
            düğme.addActionListener(Olay -> { bas_değer = true; doğrulamak(); });
            Pencere.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            Pencere.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent Olay) { tuş_artış = true; doğrulamak(); }
            });
            Pencere.add(düğme);
            Pencere.setSize(600, 180);
            Pencere.setLocation(120, 120);
            Pencere.setAlwaysOnTop(true);
            Pencere.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            Pencere.setVisible(true);
            Pencere.toFront();
            Timer Hazırlan = new Timer(750, Olay -> {
                Point konum = düğme.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (konum.x + düğme.getWidth() / 2)
                        + " " + (konum.y + düğme.getHeight() / 2));
            });
            Hazırlan.setRepeats(false);
            Hazırlan.start();
        });
    }
}
