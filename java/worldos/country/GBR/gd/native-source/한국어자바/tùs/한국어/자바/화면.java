// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable Gnìomh) { SwingUtilities.invokeLater(Gnìomh); }
    /** Swing 이벤트 Pròiseas_VALUE_cur_a_steach 가닥에서 호출한다. */
    public static JFrame uinneag(String uinneag_tiotal, JComponent susbaint_VALUE, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame uinneag = new JFrame(uinneag_tiotal);
        uinneag.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        uinneag.setContentPane(susbaint_VALUE);
        uinneag.setSize(너비, 높이);
        uinneag.setLocationByPlatform(true);
        uinneag.setVisible(true);
        return uinneag;
    }
}
