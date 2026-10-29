// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class grafika_vstup_test {
    private static boolean Klíč_vstup, 누름;
    private static JFrame Okno;

    private static void ověřit() {
        if (Klíč_vstup && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            Okno.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window cílová_úroveň : Window.getWindows()) {
                        if (cílová_úroveň instanceof JFrame && cílová_úroveň.isVisible()
                                && ((JFrame) cílová_úroveň).getTitle().equals("다국어 인사")) {
                            cílová_úroveň.toFront();
                            new Thread(() -> {
                                try {
                                    Robot synchronizovat = new Robot();
                                    synchronizovat.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception chyba) {
                                    throw new RuntimeException(chyba);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception chyba) {
                throw new RuntimeException(chyba);
            }
        }
    }

    public static void main(String[] argumenty) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            Okno = new JFrame("QEMU 키보드·마우스 zkoušky");
            JButton tlačítko = new JButton("한글 화면 · 이 단추를 누르고 K를 vstup_HODNOTA");
            tlačítko.addActionListener(Události -> { 누름 = true; ověřit(); });
            Okno.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            Okno.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent Události) { Klíč_vstup = true; ověřit(); }
            });
            Okno.add(tlačítko);
            Okno.setSize(600, 180);
            Okno.setLocation(120, 120);
            Okno.setAlwaysOnTop(true);
            Okno.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            Okno.setVisible(true);
            Okno.toFront();
            Timer Připravit = new Timer(750, Události -> {
                Point pozice = tlačítko.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (pozice.x + tlačítko.getWidth() / 2)
                        + " " + (pozice.y + tlačítko.getHeight() / 2));
            });
            Připravit.setRepeats(false);
            Připravit.start();
        });
    }
}
