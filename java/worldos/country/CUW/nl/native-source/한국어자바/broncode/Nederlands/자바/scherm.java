// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nederlands.자바;

import javax.swing.*;

public final class scherm {
    private scherm() {}
    public static void 나중에(Runnable Actie) { SwingUtilities.invokeLater(Actie); }
    /** Swing 이벤트 Proces_WAARDE_invoer 가닥에서 호출한다. */
    public static JFrame Venster(String venster_Titel, JComponent Inhoud_WAARDE, int 너비, int hoogte_WAARDE) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("scherm.나중에 안에서 창을 만드세요");
        JFrame Venster = new JFrame(venster_Titel);
        Venster.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Venster.setContentPane(Inhoud_WAARDE);
        Venster.setSize(너비, hoogte_WAARDE);
        Venster.setLocationByPlatform(true);
        Venster.setVisible(true);
        return Venster;
    }
}
