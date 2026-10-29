// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable നടപടി) { SwingUtilities.invokeLater(നടപടി); }
    /** Swing 이벤트 പ്രോസസ്_മൂല്യം_എന്_ട്രി 가닥에서 호출한다. */
    public static JFrame ജാലകം(String ജാലകം_ശീർഷകം, JComponent ഉള്ളടക്കം_മൂല്യം, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame ജാലകം = new JFrame(ജാലകം_ശീർഷകം);
        ജാലകം.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        ജാലകം.setContentPane(ഉള്ളടക്കം_മൂല്യം);
        ജാലകം.setSize(너비, 높이);
        ജാലകം.setLocationByPlatform(true);
        ജാലകം.setVisible(true);
        return ജാലകം;
    }
}
