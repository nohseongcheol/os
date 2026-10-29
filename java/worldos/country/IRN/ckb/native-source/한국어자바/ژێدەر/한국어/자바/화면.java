// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable ئاکشن) { SwingUtilities.invokeLater(ئاکشن); }
    /** Swing 이벤트 پرۆسە_نرخ_تێنووسین 가닥에서 호출한다. */
    public static JFrame پەنجەرە(String پەنجەرە_سەردێڕ, JComponent ناوەرۆک_نرخ, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame پەنجەرە = new JFrame(پەنجەرە_سەردێڕ);
        پەنجەرە.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        پەنجەرە.setContentPane(ناوەرۆک_نرخ);
        پەنجەرە.setSize(너비, 높이);
        پەنجەرە.setLocationByPlatform(true);
        پەنجەرە.setVisible(true);
        return پەنجەرە;
    }
}
