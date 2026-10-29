// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package norsk.자바;

import javax.swing.*;

public final class skjermbilde {
    private skjermbilde() {}
    public static void 나중에(Runnable Handling) { SwingUtilities.invokeLater(Handling); }
    /** Swing 이벤트 Prosess_VERDI_oppføring 가닥에서 호출한다. */
    public static JFrame Vindu(String vindu_Tittel, JComponent Innhold_VERDI, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("skjermbilde.나중에 안에서 창을 만드세요");
        JFrame Vindu = new JFrame(vindu_Tittel);
        Vindu.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Vindu.setContentPane(Innhold_VERDI);
        Vindu.setSize(너비, 높이);
        Vindu.setLocationByPlatform(true);
        Vindu.setVisible(true);
        return Vindu;
    }
}
