// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable aksyon) { SwingUtilities.invokeLater(aksyon); }
    /** Swing 이벤트 Proseso_VALUE_pagpasok 가닥에서 호출한다. */
    public static JFrame window(String window_Pamagat, JComponent Nilalaman_VALUE, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame window = new JFrame(window_Pamagat);
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.setContentPane(Nilalaman_VALUE);
        window.setSize(너비, 높이);
        window.setLocationByPlatform(true);
        window.setVisible(true);
        return window;
    }
}
