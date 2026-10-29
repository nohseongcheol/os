// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package polski.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable Akcja) { SwingUtilities.invokeLater(Akcja); }
    /** Swing 이벤트 Proces_WARTOŚĆ_wpis 가닥에서 호출한다. */
    public static JFrame Okno(String okno_Tytuł, JComponent treść_WARTOŚĆ_cb0f2404, int 너비, int wysokość_WARTOŚĆ) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame Okno = new JFrame(okno_Tytuł);
        Okno.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Okno.setContentPane(treść_WARTOŚĆ_cb0f2404);
        Okno.setSize(너비, wysokość_WARTOŚĆ);
        Okno.setLocationByPlatform(true);
        Okno.setVisible(true);
        return Okno;
    }
}
