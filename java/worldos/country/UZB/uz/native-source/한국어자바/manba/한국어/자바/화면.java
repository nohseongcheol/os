// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable Amal) { SwingUtilities.invokeLater(Amal); }
    /** Swing 이벤트 Jarayon_VALUE_kiritish 가닥에서 호출한다. */
    public static JFrame oyna(String oyna_Nom, JComponent tarkib_VALUE, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame oyna = new JFrame(oyna_Nom);
        oyna.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        oyna.setContentPane(tarkib_VALUE);
        oyna.setSize(너비, 높이);
        oyna.setLocationByPlatform(true);
        oyna.setVisible(true);
        return oyna;
    }
}
