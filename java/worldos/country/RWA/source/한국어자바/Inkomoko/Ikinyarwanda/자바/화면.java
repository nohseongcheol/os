// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ikinyarwanda.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable Igikorwa) { SwingUtilities.invokeLater(Igikorwa); }
    /** Swing 이벤트 Inzira_agaciro_icyinjizwa 가닥에서 호출한다. */
    public static JFrame idirishya(String idirishya_Umutwe, JComponent Ibirimo_agaciro, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame idirishya = new JFrame(idirishya_Umutwe);
        idirishya.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        idirishya.setContentPane(Ibirimo_agaciro);
        idirishya.setSize(너비, 높이);
        idirishya.setLocationByPlatform(true);
        idirishya.setVisible(true);
        return idirishya;
    }
}
