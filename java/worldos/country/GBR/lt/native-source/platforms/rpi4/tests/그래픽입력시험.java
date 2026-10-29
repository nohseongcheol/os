// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class 그래픽입력시험 {
    private static boolean 키입력, paspausti_VALUE;
    private static JFrame Langas;

    private static void patvirtinti() {
        if (키입력 && paspausti_VALUE) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            Langas.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window tikslas : Window.getWindows()) {
                        if (tikslas instanceof JFrame && tikslas.isVisible()
                                && ((JFrame) tikslas).getTitle().equals("다국어 인사")) {
                            tikslas.toFront();
                            new Thread(() -> {
                                try {
                                    Robot sinchronizuoti = new Robot();
                                    sinchronizuoti.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception KLAIDA) {
                                    throw new RuntimeException(KLAIDA);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception KLAIDA) {
                throw new RuntimeException(KLAIDA);
            }
        }
    }

    public static void main(String[] Argumentai) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            Langas = new JFrame("QEMU 키보드·마우스 시험");
            JButton mygtukas = new JButton("한글 화면 · 이 단추를 누르고 K를 입력");
            mygtukas.addActionListener(Įvykis -> { paspausti_VALUE = true; patvirtinti(); });
            Langas.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            Langas.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent Įvykis) { 키입력 = true; patvirtinti(); }
            });
            Langas.add(mygtukas);
            Langas.setSize(600, 180);
            Langas.setLocation(120, 120);
            Langas.setAlwaysOnTop(true);
            Langas.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            Langas.setVisible(true);
            Langas.toFront();
            Timer Parengti = new Timer(750, Įvykis -> {
                Point Pozicija = mygtukas.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (Pozicija.x + mygtukas.getWidth() / 2)
                        + " " + (Pozicija.y + mygtukas.getHeight() / 2));
            });
            Parengti.setRepeats(false);
            Parengti.start();
        });
    }
}
