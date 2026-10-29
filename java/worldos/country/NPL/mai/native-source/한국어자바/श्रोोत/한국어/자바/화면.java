// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable क्रिया) { SwingUtilities.invokeLater(क्रिया); }
    /** Swing 이벤트 처리 가닥에서 호출한다. */
    public static JFrame 창(String 제목, JComponent 내용, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame 창 = new JFrame(제목);
        창.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        창.setContentPane(내용);
        창.setSize(너비, 높이);
        창.setLocationByPlatform(true);
        창.setVisible(true);
        return 창;
    }
}
