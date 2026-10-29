// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eesti.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable Nimi) { SwingUtilities.invokeLater(Nimi); }
    /** Swing 이벤트 Joonis_VALUE_kirje 가닥에서 호출한다. */
    public static JFrame aken(String aken_teos, JComponent Sisu_VALUE, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame aken = new JFrame(aken_teos);
        aken.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        aken.setContentPane(Sisu_VALUE);
        aken.setSize(너비, 높이);
        aken.setLocationByPlatform(true);
        aken.setVisible(true);
        return aken;
    }
}
