// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Македонски.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable Дејство) { SwingUtilities.invokeLater(Дејство); }
    /** Swing 이벤트 Процес_VALUE_внес 가닥에서 호출한다. */
    public static JFrame прозорец(String прозорец_Наслов, JComponent Содржина_VALUE, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame прозорец = new JFrame(прозорец_Наслов);
        прозорец.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        прозорец.setContentPane(Содржина_VALUE);
        прозорец.setSize(너비, 높이);
        прозорец.setLocationByPlatform(true);
        прозорец.setVisible(true);
        return прозорец;
    }
}
