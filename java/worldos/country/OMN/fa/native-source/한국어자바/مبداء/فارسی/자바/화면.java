// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package فارسی.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable کنش) { SwingUtilities.invokeLater(کنش); }
    /** Swing 이벤트 فرآیند_مقدار_ورودی 가닥에서 호출한다. */
    public static JFrame پنجره(String پنجره_عنوان, JComponent محتوا_مقدار, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame پنجره = new JFrame(پنجره_عنوان);
        پنجره.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        پنجره.setContentPane(محتوا_مقدار);
        پنجره.setSize(너비, 높이);
        پنجره.setLocationByPlatform(true);
        پنجره.setVisible(true);
        return پنجره;
    }
}
