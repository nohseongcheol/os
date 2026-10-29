// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable Дзеянне) { SwingUtilities.invokeLater(Дзеянне); }
    /** Swing 이벤트 Працэс_значэнне_увядзенне 가닥에서 호출한다. */
    public static JFrame акно(String акно_Загаловак, JComponent кантэнт_значэнне, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame акно = new JFrame(акно_Загаловак);
        акно.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        акно.setContentPane(кантэнт_значэнне);
        акно.setSize(너비, 높이);
        акно.setLocationByPlatform(true);
        акно.setVisible(true);
        return акно;
    }
}
