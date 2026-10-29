// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class GrafikEingabePrüfung {
    private static boolean tasteEingabe, drückenWert;
    private static JFrame fenster;

    private static void überprüfen() {
        if (tasteEingabe && drückenWert) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            fenster.dispose();
            try {
                Class.forName("Gruß").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window zielobjektWert : Window.getWindows()) {
                        if (zielobjektWert instanceof JFrame && zielobjektWert.isVisible()
                                && ((JFrame) zielobjektWert).getTitle().equals("다국어 Gruß")) {
                            zielobjektWert.toFront();
                            new Thread(() -> {
                                try {
                                    Robot synchronisieren = new Robot();
                                    synchronisieren.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception fehler) {
                                    throw new RuntimeException(fehler);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("Gruß 창이 표시되지 않았습니다");
                });
            } catch (Exception fehler) {
                throw new RuntimeException(fehler);
            }
        }
    }

    public static void main(String[] argumente) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 Bildschirm fehlendMethode");
        SwingUtilities.invokeAndWait(() -> {
            fenster = new JFrame("QEMU 키보드·마우스 Prüfungen");
            JButton schaltfläche = new JButton("한글 Bildschirm · 이 단추를 누르고 K를 Eingabewert");
            schaltfläche.addActionListener(ereignis -> { drückenWert = true; überprüfen(); });
            fenster.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            fenster.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent ereignis) { tasteEingabe = true; überprüfen(); }
            });
            fenster.add(schaltfläche);
            fenster.setSize(600, 180);
            fenster.setLocation(120, 120);
            fenster.setAlwaysOnTop(true);
            fenster.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            fenster.setVisible(true);
            fenster.toFront();
            Timer vorbereiten = new Timer(750, ereignis -> {
                Point position = schaltfläche.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (position.x + schaltfläche.getWidth() / 2)
                        + " " + (position.y + schaltfläche.getHeight() / 2));
            });
            vorbereiten.setRepeats(false);
            vorbereiten.start();
        });
    }
}
