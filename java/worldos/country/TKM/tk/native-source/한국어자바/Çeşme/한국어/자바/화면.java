// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable iş) { SwingUtilities.invokeLater(iş); }
    /** Swing 이벤트 Proses_baha_girizmeklik 가닥에서 호출한다. */
    public static JFrame penjire(String penjire_Ady, JComponent Mazmun_baha, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame penjire = new JFrame(penjire_Ady);
        penjire.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        penjire.setContentPane(Mazmun_baha);
        penjire.setSize(너비, 높이);
        penjire.setLocationByPlatform(true);
        penjire.setVisible(true);
        return penjire;
    }
}
