// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.Java;

import javax.swing.*;

public final class Bildschirm {
    private Bildschirm() {}
    public static void späterWert(Runnable aktion) { SwingUtilities.invokeLater(aktion); }
    /** Auf dem Swing-Ereignisverteilungsfaden aufrufen. */
    public static JFrame fenster(String fensterTitel, JComponent inhaltswertWert, int breiteWert, int höheWert) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("Bildschirm.späterWert 안에서 창을 만드세요");
        JFrame fenster = new JFrame(fensterTitel);
        fenster.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        fenster.setContentPane(inhaltswertWert);
        fenster.setSize(breiteWert, höheWert);
        fenster.setLocationByPlatform(true);
        fenster.setVisible(true);
        return fenster;
    }
}
