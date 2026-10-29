// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class γραφικά_είσοδος_δοκιμή {
    private static boolean Κλειδί_είσοδος, 누름;
    private static JFrame Παράθυρο;

    private static void επαληθεύω() {
        if (Κλειδί_είσοδος && 누름) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            Παράθυρο.dispose();
            try {
                Class.forName("인사").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window τιμή_στόχος : Window.getWindows()) {
                        if (τιμή_στόχος instanceof JFrame && τιμή_στόχος.isVisible()
                                && ((JFrame) τιμή_στόχος).getTitle().equals("다국어 인사")) {
                            τιμή_στόχος.toFront();
                            new Thread(() -> {
                                try {
                                    Robot συγχρονίζω = new Robot();
                                    συγχρονίζω.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception ΣΦΑΛΜΑ) {
                                    throw new RuntimeException(ΣΦΑΛΜΑ);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("인사 창이 표시되지 않았습니다");
                });
            } catch (Exception ΣΦΑΛΜΑ) {
                throw new RuntimeException(ΣΦΑΛΜΑ);
            }
        }
    }

    public static void main(String[] Παράμετροι) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 화면 없음");
        SwingUtilities.invokeAndWait(() -> {
            Παράθυρο = new JFrame("QEMU 키보드·마우스 시험");
            JButton κουμπί = new JButton("한글 화면 · 이 단추를 누르고 K를 είσοδος_τιμή");
            κουμπί.addActionListener(Συμβάν -> { 누름 = true; επαληθεύω(); });
            Παράθυρο.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            Παράθυρο.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent Συμβάν) { Κλειδί_είσοδος = true; επαληθεύω(); }
            });
            Παράθυρο.add(κουμπί);
            Παράθυρο.setSize(600, 180);
            Παράθυρο.setLocation(120, 120);
            Παράθυρο.setAlwaysOnTop(true);
            Παράθυρο.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            Παράθυρο.setVisible(true);
            Παράθυρο.toFront();
            Timer Προετοίμασε = new Timer(750, Συμβάν -> {
                Point Θέση = κουμπί.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (Θέση.x + κουμπί.getWidth() / 2)
                        + " " + (Θέση.y + κουμπί.getHeight() / 2));
            });
            Προετοίμασε.setRepeats(false);
            Προετοίμασε.start();
        });
    }
}
