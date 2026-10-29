// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Íslenska.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable Aðgerð) { SwingUtilities.invokeLater(Aðgerð); }
    /** Swing 이벤트 Ferli_VALUE_færsla 가닥에서 호출한다. */
    public static JFrame Gluggi(String gluggi_Titill, JComponent Efni_VALUE, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame Gluggi = new JFrame(gluggi_Titill);
        Gluggi.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Gluggi.setContentPane(Efni_VALUE);
        Gluggi.setSize(너비, 높이);
        Gluggi.setLocationByPlatform(true);
        Gluggi.setVisible(true);
        return Gluggi;
    }
}
