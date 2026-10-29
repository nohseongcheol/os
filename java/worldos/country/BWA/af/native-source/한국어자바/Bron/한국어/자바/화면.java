// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable Aksie) { SwingUtilities.invokeLater(Aksie); }
    /** Swing 이벤트 Proses_VALUE_inskrywing 가닥에서 호출한다. */
    public static JFrame venster(String venster_Titel, JComponent Inhoud_VALUE, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame venster = new JFrame(venster_Titel);
        venster.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        venster.setContentPane(Inhoud_VALUE);
        venster.setSize(너비, 높이);
        venster.setLocationByPlatform(true);
        venster.setVisible(true);
        return venster;
    }
}
