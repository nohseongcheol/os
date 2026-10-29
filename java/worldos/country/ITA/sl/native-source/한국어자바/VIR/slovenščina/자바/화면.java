// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package slovenščina.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable Dejanje) { SwingUtilities.invokeLater(Dejanje); }
    /** Swing 이벤트 Proces_VALUE_vnos 가닥에서 호출한다. */
    public static JFrame okno(String okno_naslov, JComponent vsebina_VALUE, int 너비, int višina_VALUE) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame okno = new JFrame(okno_naslov);
        okno.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        okno.setContentPane(vsebina_VALUE);
        okno.setSize(너비, višina_VALUE);
        okno.setLocationByPlatform(true);
        okno.setVisible(true);
        return okno;
    }
}
