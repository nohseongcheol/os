// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable Veprim) { SwingUtilities.invokeLater(Veprim); }
    /** Swing 이벤트 Proces_VALUE_futje 가닥에서 호출한다. */
    public static JFrame Dritare(String dritare_Titulli, JComponent Përmbajtje_VALUE, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame Dritare = new JFrame(dritare_Titulli);
        Dritare.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Dritare.setContentPane(Përmbajtje_VALUE);
        Dritare.setSize(너비, 높이);
        Dritare.setLocationByPlatform(true);
        Dritare.setVisible(true);
        return Dritare;
    }
}
