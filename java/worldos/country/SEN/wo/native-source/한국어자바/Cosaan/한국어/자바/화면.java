// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable jëf) { SwingUtilities.invokeLater(jëf); }
    /** Swing 이벤트 yokkute_xëyma_dugal_xabaar 가닥에서 호출한다. */
    public static JFrame palanteer(String palanteer_Tur, JComponent Këmb_xëyma, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame palanteer = new JFrame(palanteer_Tur);
        palanteer.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        palanteer.setContentPane(Këmb_xëyma);
        palanteer.setSize(너비, 높이);
        palanteer.setLocationByPlatform(true);
        palanteer.setVisible(true);
        return palanteer;
    }
}
