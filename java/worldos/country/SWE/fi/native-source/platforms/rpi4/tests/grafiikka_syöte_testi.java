// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class grafiikka_syöte_testi {
    private static boolean Avain_syöte, paina_ARVO;
    private static JFrame Ikkuna;

    private static void tarkistaa() {
        if (Avain_syöte && paina_ARVO) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            Ikkuna.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window tavoite : Window.getWindows()) {
                        if (tavoite instanceof JFrame && tavoite.isVisible()
                                && ((JFrame) tavoite).getTitle().equals("다국어 인사")) {
                            tavoite.toFront();
                            new Thread(() -> {
                                try {
                                    Robot synkronoi = new Robot();
                                    synkronoi.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception VIRHE) {
                                    throw new RuntimeException(VIRHE);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception VIRHE) {
                throw new RuntimeException(VIRHE);
            }
        }
    }

    public static void main(String[] argumentit) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            Ikkuna = new JFrame("QEMU 키보드·마우스 testit");
            JButton painike = new JButton("한글 화면 · 이 단추를 누르고 K를 syöte_ARVO");
            painike.addActionListener(Tapahtuma -> { paina_ARVO = true; tarkistaa(); });
            Ikkuna.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            Ikkuna.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent Tapahtuma) { Avain_syöte = true; tarkistaa(); }
            });
            Ikkuna.add(painike);
            Ikkuna.setSize(600, 180);
            Ikkuna.setLocation(120, 120);
            Ikkuna.setAlwaysOnTop(true);
            Ikkuna.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            Ikkuna.setVisible(true);
            Ikkuna.toFront();
            Timer Valmistele = new Timer(750, Tapahtuma -> {
                Point paikka = painike.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (paikka.x + painike.getWidth() / 2)
                        + " " + (paikka.y + painike.getHeight() / 2));
            });
            Valmistele.setRepeats(false);
            Valmistele.start();
        });
    }
}
