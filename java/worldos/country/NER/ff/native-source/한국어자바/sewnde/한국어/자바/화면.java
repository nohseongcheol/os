// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable gollal) { SwingUtilities.invokeLater(gollal); }
    /** Swing 이벤트 Yuɓɓo_golle_njaru_naatnugol 가닥에서 호출한다. */
    public static JFrame falanteere(String 제목, JComponent loowdi_njaru, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame falanteere = new JFrame(제목);
        falanteere.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        falanteere.setContentPane(loowdi_njaru);
        falanteere.setSize(너비, 높이);
        falanteere.setLocationByPlatform(true);
        falanteere.setVisible(true);
        return falanteere;
    }
}
