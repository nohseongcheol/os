// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package magyar.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable Művelet) { SwingUtilities.invokeLater(Művelet); }
    /** Swing 이벤트 folyamat_ÉRTÉK_bejegyzés 가닥에서 호출한다. */
    public static JFrame Ablak(String ablak_Cím, JComponent Tartalom_ÉRTÉK, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame Ablak = new JFrame(ablak_Cím);
        Ablak.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Ablak.setContentPane(Tartalom_ÉRTÉK);
        Ablak.setSize(너비, 높이);
        Ablak.setLocationByPlatform(true);
        Ablak.setVisible(true);
        return Ablak;
    }
}
