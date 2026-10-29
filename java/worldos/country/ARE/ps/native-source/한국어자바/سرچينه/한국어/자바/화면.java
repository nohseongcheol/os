// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable چار) { SwingUtilities.invokeLater(چار); }
    /** Swing 이벤트 처리 가닥에서 호출한다. */
    public static JFrame کړکۍ(String 제목, JComponent منځپانګه_ارزښت, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame کړکۍ = new JFrame(제목);
        کړکۍ.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        کړکۍ.setContentPane(منځپانګه_ارزښت);
        کړکۍ.setSize(너비, 높이);
        کړکۍ.setLocationByPlatform(true);
        کړکۍ.setVisible(true);
        return کړکۍ;
    }
}
