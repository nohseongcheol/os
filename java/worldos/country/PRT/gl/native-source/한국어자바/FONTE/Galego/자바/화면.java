// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Galego.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable Acción) { SwingUtilities.invokeLater(Acción); }
    /** Swing 이벤트 Proceso_VALOR_introdución 가닥에서 호출한다. */
    public static JFrame Xanela(String ventá_Título, JComponent Contido_VALOR, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame Xanela = new JFrame(ventá_Título);
        Xanela.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Xanela.setContentPane(Contido_VALOR);
        Xanela.setSize(너비, 높이);
        Xanela.setLocationByPlatform(true);
        Xanela.setVisible(true);
        return Xanela;
    }
}
