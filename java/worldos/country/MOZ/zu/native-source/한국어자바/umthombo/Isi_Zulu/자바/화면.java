// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Isi_Zulu.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable Isenzo) { SwingUtilities.invokeLater(Isenzo); }
    /** Swing 이벤트 Inqubo_inani_okufakwayo 가닥에서 호출한다. */
    public static JFrame ifasitela(String ifasitela_Isihloko, JComponent Okuqukethwe_inani, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame ifasitela = new JFrame(ifasitela_Isihloko);
        ifasitela.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        ifasitela.setContentPane(Okuqukethwe_inani);
        ifasitela.setSize(너비, 높이);
        ifasitela.setLocationByPlatform(true);
        ifasitela.setVisible(true);
        return ifasitela;
    }
}
