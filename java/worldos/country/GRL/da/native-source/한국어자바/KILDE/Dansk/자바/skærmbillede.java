// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Dansk.자바;

import javax.swing.*;

public final class skærmbillede {
    private skærmbillede() {}
    public static void 나중에(Runnable Handling) { SwingUtilities.invokeLater(Handling); }
    /** Swing 이벤트 Proces_VÆRDI_post 가닥에서 호출한다. */
    public static JFrame Vindue(String vindue_Titel, JComponent Indhold_VÆRDI, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("skærmbillede.나중에 안에서 창을 만드세요");
        JFrame Vindue = new JFrame(vindue_Titel);
        Vindue.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Vindue.setContentPane(Indhold_VÆRDI);
        Vindue.setSize(너비, 높이);
        Vindue.setLocationByPlatform(true);
        Vindue.setVisible(true);
        return Vindue;
    }
}
