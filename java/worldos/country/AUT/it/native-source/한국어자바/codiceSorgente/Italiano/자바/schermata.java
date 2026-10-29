// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Italiano.자바;

import javax.swing.*;

public final class schermata {
    private schermata() {}
    public static void 나중에(Runnable Azione) { SwingUtilities.invokeLater(Azione); }
    /** Swing 이벤트 Processi_VALORE_voce 가닥에서 호출한다. */
    public static JFrame Finestra(String finestra_titolo, JComponent Contenuto_VALORE, int 너비, int altezza_VALORE) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("schermata.나중에 안에서 창을 만드세요");
        JFrame Finestra = new JFrame(finestra_titolo);
        Finestra.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Finestra.setContentPane(Contenuto_VALORE);
        Finestra.setSize(너비, altezza_VALORE);
        Finestra.setLocationByPlatform(true);
        Finestra.setVisible(true);
        return Finestra;
    }
}
