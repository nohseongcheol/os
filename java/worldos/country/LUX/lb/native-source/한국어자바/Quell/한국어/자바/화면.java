// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable Aktioun) { SwingUtilities.invokeLater(Aktioun); }
    /** Swing 이벤트 Prozess_VALUE_Agab 가닥에서 호출한다. */
    public static JFrame Fënster(String Fënster_Titel, JComponent Inhalt_VALUE, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame Fënster = new JFrame(Fënster_Titel);
        Fënster.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Fënster.setContentPane(Inhalt_VALUE);
        Fënster.setSize(너비, 높이);
        Fënster.setLocationByPlatform(true);
        Fënster.setVisible(true);
        return Fënster;
    }
}
