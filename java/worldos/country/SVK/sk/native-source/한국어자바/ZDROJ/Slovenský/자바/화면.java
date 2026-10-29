// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovenský.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable Akcia) { SwingUtilities.invokeLater(Akcia); }
    /** Swing 이벤트 Proces_VALUE_položka 가닥에서 호출한다. */
    public static JFrame Okno(String okno_Názov, JComponent obsah_VALUE, int 너비, int výška_VALUE) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame Okno = new JFrame(okno_Názov);
        Okno.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Okno.setContentPane(obsah_VALUE);
        Okno.setSize(너비, výška_VALUE);
        Okno.setLocationByPlatform(true);
        Okno.setVisible(true);
        return Okno;
    }
}
