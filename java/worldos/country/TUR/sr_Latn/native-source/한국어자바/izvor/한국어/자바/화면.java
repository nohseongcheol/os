// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable radnja) { SwingUtilities.invokeLater(radnja); }
    /** Swing 이벤트 Proces_VALUE_stavka 가닥에서 호출한다. */
    public static JFrame prozor(String prozor_Naslov, JComponent Sadržaj_VALUE, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame prozor = new JFrame(prozor_Naslov);
        prozor.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        prozor.setContentPane(Sadržaj_VALUE);
        prozor.setSize(너비, 높이);
        prozor.setLocationByPlatform(true);
        prozor.setVisible(true);
        return prozor;
    }
}
