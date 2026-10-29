// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package suomi.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable Toiminto) { SwingUtilities.invokeLater(Toiminto); }
    /** Swing 이벤트 prosessi_ARVO_merkintä 가닥에서 호출한다. */
    public static JFrame Ikkuna(String ikkuna_nimi, JComponent Sisältö_ARVO, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame Ikkuna = new JFrame(ikkuna_nimi);
        Ikkuna.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Ikkuna.setContentPane(Sisältö_ARVO);
        Ikkuna.setSize(너비, 높이);
        Ikkuna.setLocationByPlatform(true);
        Ikkuna.setVisible(true);
        return Ikkuna;
    }
}
