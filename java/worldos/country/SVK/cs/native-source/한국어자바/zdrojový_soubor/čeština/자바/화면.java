// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package čeština.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable Akce) { SwingUtilities.invokeLater(Akce); }
    /** Swing 이벤트 Proces_HODNOTA_položka 가닥에서 호출한다. */
    public static JFrame Okno(String okno_Název, JComponent Obsah_HODNOTA, int 너비, int výška_HODNOTA) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame Okno = new JFrame(okno_Název);
        Okno.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Okno.setContentPane(Obsah_HODNOTA);
        Okno.setSize(너비, výška_HODNOTA);
        Okno.setLocationByPlatform(true);
        Okno.setVisible(true);
        return Okno;
    }
}
