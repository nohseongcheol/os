// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package isiXhosa.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable Intshukumo) { SwingUtilities.invokeLater(Intshukumo); }
    /** Swing 이벤트 Inkqubo_ixabiso_ufako_nkcukacha 가닥에서 호출한다. */
    public static JFrame i_window(String i_window_Isihloko, JComponent Isiqulatho_ixabiso, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame i_window = new JFrame(i_window_Isihloko);
        i_window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        i_window.setContentPane(Isiqulatho_ixabiso);
        i_window.setSize(너비, 높이);
        i_window.setLocationByPlatform(true);
        i_window.setVisible(true);
        return i_window;
    }
}
