// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Reo_Māori.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable hohenga) { SwingUtilities.invokeLater(hohenga); }
    /** Swing 이벤트 Hātepe_uara_tāurunga 가닥에서 호출한다. */
    public static JFrame matapihi(String matapihi_Taitara, JComponent Ihirangi_uara, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame matapihi = new JFrame(matapihi_Taitara);
        matapihi.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        matapihi.setContentPane(Ihirangi_uara);
        matapihi.setSize(너비, 높이);
        matapihi.setLocationByPlatform(true);
        matapihi.setVisible(true);
        return matapihi;
    }
}
