// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class grafické_prvky_vstup_test {
    private static boolean Kľúč_vstup, 누름;
    private static JFrame Okno;

    private static void overiť() {
        if (Kľúč_vstup && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            Okno.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window cieľová_hodnota : Window.getWindows()) {
                        if (cieľová_hodnota instanceof JFrame && cieľová_hodnota.isVisible()
                                && ((JFrame) cieľová_hodnota).getTitle().equals("다국어 인사")) {
                            cieľová_hodnota.toFront();
                            new Thread(() -> {
                                try {
                                    Robot synchronizovať = new Robot();
                                    synchronizovať.waitForIdle();
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

    public static void main(String[] Argumenty) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            Okno = new JFrame("QEMU 키보드·마우스 시험");
            JButton Tlačidlo = new JButton("한글 화면 · 이 단추를 누르고 K를 vstup_VALUE");
            Tlačidlo.addActionListener(Udalosť -> { 누름 = true; overiť(); });
            Okno.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            Okno.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent Udalosť) { Kľúč_vstup = true; overiť(); }
            });
            Okno.add(Tlačidlo);
            Okno.setSize(600, 180);
            Okno.setLocation(120, 120);
            Okno.setAlwaysOnTop(true);
            Okno.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            Okno.setVisible(true);
            Okno.toFront();
            Timer Pripraviť = new Timer(750, Udalosť -> {
                Point Pozícia = Tlačidlo.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (Pozícia.x + Tlačidlo.getWidth() / 2)
                        + " " + (Pozícia.y + Tlačidlo.getHeight() / 2));
            });
            Pripraviť.setRepeats(false);
            Pripraviť.start();
        });
    }
}
