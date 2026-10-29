// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable చర్య) { SwingUtilities.invokeLater(చర్య); }
    /** Swing 이벤트 విధానం_మూల్యం_ప్రవేశం 가닥에서 호출한다. */
    public static JFrame విండో(String గవాక్షం_శీర్షిక, JComponent విషయం_మూల్యం, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame విండో = new JFrame(గవాక్షం_శీర్షిక);
        విండో.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        విండో.setContentPane(విషయం_మూల్యం);
        విండో.setSize(너비, 높이);
        విండో.setLocationByPlatform(true);
        విండో.setVisible(true);
        return విండో;
    }
}
