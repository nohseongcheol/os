// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable tiro) { SwingUtilities.invokeLater(tiro); }
    /** Swing 이벤트 Thulaganyo_Boleng_tsenyo 가닥에서 호출한다. */
    public static JFrame fensetere(String fensetere_Setlhogo, JComponent Diteng_Boleng, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame fensetere = new JFrame(fensetere_Setlhogo);
        fensetere.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        fensetere.setContentPane(Diteng_Boleng);
        fensetere.setSize(너비, 높이);
        fensetere.setLocationByPlatform(true);
        fensetere.setVisible(true);
        return fensetere;
    }
}
