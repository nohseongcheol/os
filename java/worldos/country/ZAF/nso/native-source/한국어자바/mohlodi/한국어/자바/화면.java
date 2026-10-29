// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable Mogato) { SwingUtilities.invokeLater(Mogato); }
    /** Swing 이벤트 tiragalo_boleng_go_tsenya_tshedimošo 가닥에서 호출한다. */
    public static JFrame lefastere(String lefastere_Thaetlele, JComponent Diteng_boleng, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame lefastere = new JFrame(lefastere_Thaetlele);
        lefastere.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        lefastere.setContentPane(Diteng_boleng);
        lefastere.setSize(너비, 높이);
        lefastere.setLocationByPlatform(true);
        lefastere.setVisible(true);
        return lefastere;
    }
}
