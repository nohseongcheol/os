// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable радња) { SwingUtilities.invokeLater(радња); }
    /** Swing 이벤트 процес_вриједност_унос 가닥에서 호출한다. */
    public static JFrame прозор(String 제목, JComponent Садржај_вриједност, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame прозор = new JFrame(제목);
        прозор.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        прозор.setContentPane(Садржај_вриједност);
        прозор.setSize(너비, 높이);
        прозор.setLocationByPlatform(true);
        прозор.setVisible(true);
        return прозор;
    }
}
