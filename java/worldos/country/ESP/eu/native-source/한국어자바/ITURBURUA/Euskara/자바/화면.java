// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Euskara.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable Ekintza) { SwingUtilities.invokeLater(Ekintza); }
    /** Swing 이벤트 prozesu_balio_sarrera 가닥에서 호출한다. */
    public static JFrame Leihoa(String leiho_Izenburua, JComponent eduki_balio, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame Leihoa = new JFrame(leiho_Izenburua);
        Leihoa.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Leihoa.setContentPane(eduki_balio);
        Leihoa.setSize(너비, 높이);
        Leihoa.setLocationByPlatform(true);
        Leihoa.setVisible(true);
        return Leihoa;
    }
}
