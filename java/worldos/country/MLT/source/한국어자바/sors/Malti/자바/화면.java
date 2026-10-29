// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Malti.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable azzjoni) { SwingUtilities.invokeLater(azzjoni); }
    /** Swing 이벤트 Proċess_VALUE_entrata 가닥에서 호출한다. */
    public static JFrame tieqa(String tieqa_Titlu, JComponent Kontenut_VALUE, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame tieqa = new JFrame(tieqa_Titlu);
        tieqa.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        tieqa.setContentPane(Kontenut_VALUE);
        tieqa.setSize(너비, 높이);
        tieqa.setLocationByPlatform(true);
        tieqa.setVisible(true);
        return tieqa;
    }
}
