// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Svenska.자바;

import javax.swing.*;

public final class skärmbild {
    private skärmbild() {}
    public static void 나중에(Runnable Åtgärd) { SwingUtilities.invokeLater(Åtgärd); }
    /** Swing 이벤트 Process_värde_post 가닥에서 호출한다. */
    public static JFrame Fönster(String fönster_titel, JComponent Innehåll_värde, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("skärmbild.나중에 안에서 창을 만드세요");
        JFrame Fönster = new JFrame(fönster_titel);
        Fönster.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Fönster.setContentPane(Innehåll_värde);
        Fönster.setSize(너비, 높이);
        Fönster.setLocationByPlatform(true);
        Fönster.setVisible(true);
        return Fönster;
    }
}
