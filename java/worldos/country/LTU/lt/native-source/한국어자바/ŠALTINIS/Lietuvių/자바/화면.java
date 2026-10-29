// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lietuvių.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable Veiksmas) { SwingUtilities.invokeLater(Veiksmas); }
    /** Swing 이벤트 Procesas_VALUE_įrašas 가닥에서 호출한다. */
    public static JFrame Langas(String langas_Pavadinimas, JComponent Turinys_VALUE, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame Langas = new JFrame(langas_Pavadinimas);
        Langas.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Langas.setContentPane(Turinys_VALUE);
        Langas.setSize(너비, 높이);
        Langas.setLocationByPlatform(true);
        Langas.setVisible(true);
        return Langas;
    }
}
