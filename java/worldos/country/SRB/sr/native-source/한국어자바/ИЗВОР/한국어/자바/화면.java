// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable радња) { SwingUtilities.invokeLater(радња); }
    /** Swing 이벤트 처리 가닥에서 호출한다. */
    public static JFrame Прозор(String 제목, JComponent 내용, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame Прозор = new JFrame(제목);
        Прозор.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Прозор.setContentPane(내용);
        Прозор.setSize(너비, 높이);
        Прозор.setLocationByPlatform(true);
        Прозор.setVisible(true);
        return Прозор;
    }
}
