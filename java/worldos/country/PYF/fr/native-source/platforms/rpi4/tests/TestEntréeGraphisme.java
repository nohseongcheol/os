// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class TestEntréeGraphisme {
    private static boolean entréeTouche, valeurEnfoncer;
    private static JFrame fenêtre;

    private static void vérifier() {
        if (entréeTouche && valeurEnfoncer) {
            System.out.println("JKOROS_VNC_INPUT_PASS");
            fenêtre.dispose();
            try {
                Class.forName("Salutation").getMethod("main", String[].class)
                        .invoke(null, (Object) new String[0]);
                SwingUtilities.invokeLater(() -> {
                    for (Window valeurCible : Window.getWindows()) {
                        if (valeurCible instanceof JFrame && valeurCible.isVisible()
                                && ((JFrame) valeurCible).getTitle().equals("다국어 Salutation")) {
                            valeurCible.toFront();
                            new Thread(() -> {
                                try {
                                    Robot synchroniser = new Robot();
                                    synchroniser.waitForIdle();
                                    Thread.sleep(500);
                                    System.out.println("JKOROS_GREETING_VISIBLE");
                                } catch (Exception erreur) {
                                    throw new RuntimeException(erreur);
                                }
                            }).start();
                            return;
                        }
                    }
                    throw new AssertionError("Salutation 창이 표시되지 않았습니다");
                });
            } catch (Exception erreur) {
                throw new RuntimeException(erreur);
            }
        }
    }

    public static void main(String[] arguments) throws Exception {
        if (GraphicsEnvironment.isHeadless()) throw new AssertionError("그래픽 Écran méthodeManquant");
        SwingUtilities.invokeAndWait(() -> {
            fenêtre = new JFrame("QEMU 키보드·마우스 Tests");
            JButton bouton = new JButton("한글 Écran · 이 단추를 누르고 K를 valeurEntrée");
            bouton.addActionListener(évènement -> { valeurEnfoncer = true; vérifier(); });
            fenêtre.getRootPane().getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW)
                    .put(KeyStroke.getKeyStroke('k'), "키시험");
            fenêtre.getRootPane().getActionMap().put("키시험", new AbstractAction() {
                public void actionPerformed(ActionEvent évènement) { entréeTouche = true; vérifier(); }
            });
            fenêtre.add(bouton);
            fenêtre.setSize(600, 180);
            fenêtre.setLocation(120, 120);
            fenêtre.setAlwaysOnTop(true);
            fenêtre.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
            fenêtre.setVisible(true);
            fenêtre.toFront();
            Timer préparer = new Timer(750, évènement -> {
                Point position = bouton.getLocationOnScreen();
                System.out.println("JKOROS_GUI_READY " + (position.x + bouton.getWidth() / 2)
                        + " " + (position.y + bouton.getHeight() / 2));
            });
            préparer.setRepeats(false);
            préparer.start();
        });
    }
}
