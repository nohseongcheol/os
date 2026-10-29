// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable ìṣe) { SwingUtilities.invokeLater(ìṣe); }
    /** Swing 이벤트 Ìlànà_iye_ìgbéwọlé 가닥에서 호출한다. */
    public static JFrame wínńdò(String wínńdò_Àkọlé, JComponent Àkóónú_iye, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame wínńdò = new JFrame(wínńdò_Àkọlé);
        wínńdò.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        wínńdò.setContentPane(Àkóónú_iye);
        wínńdò.setSize(너비, 높이);
        wínńdò.setLocationByPlatform(true);
        wínńdò.setVisible(true);
        return wínńdò;
    }
}
