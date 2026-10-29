// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable Gedişat) { SwingUtilities.invokeLater(Gedişat); }
    /** Swing 이벤트 Proses_VALUE_daxiletmə 가닥에서 호출한다. */
    public static JFrame pəncərə(String pəncərə_Başlıq, JComponent Məzmun_VALUE, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame pəncərə = new JFrame(pəncərə_Başlıq);
        pəncərə.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        pəncərə.setContentPane(Məzmun_VALUE);
        pəncərə.setSize(너비, 높이);
        pəncərə.setLocationByPlatform(true);
        pəncərə.setVisible(true);
        return pəncərə;
    }
}
