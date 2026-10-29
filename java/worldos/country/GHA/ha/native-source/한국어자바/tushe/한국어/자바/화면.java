// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable Aiki) { SwingUtilities.invokeLater(Aiki); }
    /** Swing 이벤트 haryar_aikin_na_ura_Daraja_Mashigar_bayanai 가닥에서 호출한다. */
    public static JFrame taga(String 제목, JComponent kunshiya_Daraja, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame taga = new JFrame(제목);
        taga.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        taga.setContentPane(kunshiya_Daraja);
        taga.setSize(너비, 높이);
        taga.setLocationByPlatform(true);
        taga.setVisible(true);
        return taga;
    }
}
