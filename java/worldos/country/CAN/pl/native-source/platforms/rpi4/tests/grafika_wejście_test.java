// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class grafika_wejście_test {
    private static boolean Klucz_wejście, 누름;
    private static JFrame Okno;

    private static void 확인() {
        if (Klucz_wejście && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            Okno.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window wartość_docelowa : Window.getWindows()) {
                        if (wartość_docelowa instanceof JFrame && wartość_docelowa.isVisible()
                                && ((JFrame) wartość_docelowa).getTitle().equals("다국어 인사")) {
                            wartość_docelowa.toFront();
                            new Thread(() -> {
                                try {
                                    Robot synchronizować = new Robot();
                                    synchronizować.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception błąd) {
                                    throw new RuntimeException(błąd);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception błąd) {
                throw new RuntimeException(błąd);
            }
        }
    }

    public static void main(String[] argumenty) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            Okno = new JFrame("QEMU 키보드·마우스 testy");
            JButton przycisk = new JButton("한글 화면 · 이 단추를 누르고 K를 wejście_WARTOŚĆ");
            przycisk.addActionListener(Wydarzenie -> { 누름 = true; 확인(); });
            Okno.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            Okno.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent Wydarzenie) { Klucz_wejście = true; 확인(); }
            });
            Okno.add(przycisk);
            Okno.setSize(600, 180);
            Okno.setLocation(120, 120);
            Okno.setAlwaysOnTop(true);
            Okno.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            Okno.setVisible(true);
            Okno.toFront();
            Timer Przygotuj = new Timer(750, Wydarzenie -> {
                Point pozycja = przycisk.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (pozycja.x + przycisk.getWidth() / 2)
                        + " " + (pozycja.y + przycisk.getHeight() / 2));
            });
            Przygotuj.setRepeats(false);
            Przygotuj.start();
        });
    }
}
