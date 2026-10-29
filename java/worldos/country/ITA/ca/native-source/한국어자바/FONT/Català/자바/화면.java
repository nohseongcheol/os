// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Català.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable Acció) { SwingUtilities.invokeLater(Acció); }
    /** Swing 이벤트 Procés_VALOR_introducció 가닥에서 호출한다. */
    public static JFrame Finestra(String finestra_Títol, JComponent contingut_VALOR, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame Finestra = new JFrame(finestra_Títol);
        Finestra.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Finestra.setContentPane(contingut_VALOR);
        Finestra.setSize(너비, 높이);
        Finestra.setLocationByPlatform(true);
        Finestra.setVisible(true);
        return Finestra;
    }
}
