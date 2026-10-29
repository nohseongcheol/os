// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Cymraeg.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable Gweithrediad) { SwingUtilities.invokeLater(Gweithrediad); }
    /** Swing 이벤트 Proses_VALUE_cofnod 가닥에서 호출한다. */
    public static JFrame ffenestr(String ffenestr_Teitl, JComponent Cynnwys_VALUE, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame ffenestr = new JFrame(ffenestr_Teitl);
        ffenestr.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        ffenestr.setContentPane(Cynnwys_VALUE);
        ffenestr.setSize(너비, 높이);
        ffenestr.setLocationByPlatform(true);
        ffenestr.setVisible(true);
        return ffenestr;
    }
}
