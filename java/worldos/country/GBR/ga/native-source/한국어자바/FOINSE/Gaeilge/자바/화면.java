// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Gaeilge.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable Gníomh) { SwingUtilities.invokeLater(Gníomh); }
    /** Swing 이벤트 Próiseas_VALUE_iontráil 가닥에서 호출한다. */
    public static JFrame fuinneog(String fuinneog_Teideal, JComponent Inneachar_VALUE, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame fuinneog = new JFrame(fuinneog_Teideal);
        fuinneog.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        fuinneog.setContentPane(Inneachar_VALUE);
        fuinneog.setSize(너비, 높이);
        fuinneog.setLocationByPlatform(true);
        fuinneog.setVisible(true);
        return fuinneog;
    }
}
