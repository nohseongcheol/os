// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable sugiarut) { SwingUtilities.invokeLater(sugiarut); }
    /** Swing 이벤트 Pivallianiq_atuutilik_Iliniku 가닥에서 호출한다. */
    public static JFrame igalaangujaq(String 제목, JComponent Ilulingit_atuutilik, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame igalaangujaq = new JFrame(제목);
        igalaangujaq.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        igalaangujaq.setContentPane(Ilulingit_atuutilik);
        igalaangujaq.setSize(너비, 높이);
        igalaangujaq.setLocationByPlatform(true);
        igalaangujaq.setVisible(true);
        return igalaangujaq;
    }
}
