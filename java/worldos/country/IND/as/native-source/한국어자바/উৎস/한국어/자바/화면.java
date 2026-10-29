// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable কাৰ্য্য) { SwingUtilities.invokeLater(কাৰ্য্য); }
    /** Swing 이벤트 প্ৰক্ৰিয়া_মান_প্রবিষ্ট 가닥에서 호출한다. */
    public static JFrame উইণ্ড(String উইণ্ড_শিৰোনাম, JComponent সামগ্ৰী_মান, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame উইণ্ড = new JFrame(উইণ্ড_শিৰোনাম);
        উইণ্ড.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        উইণ্ড.setContentPane(সামগ্ৰী_মান);
        উইণ্ড.setSize(너비, 높이);
        উইণ্ড.setLocationByPlatform(true);
        উইণ্ড.setVisible(true);
        return উইণ্ড;
    }
}
