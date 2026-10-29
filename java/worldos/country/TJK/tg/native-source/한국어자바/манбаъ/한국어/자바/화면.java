// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable Амал) { SwingUtilities.invokeLater(Амал); }
    /** Swing 이벤트 Раванд_қимат_ворида 가닥에서 호출한다. */
    public static JFrame равзана(String равзана_Унвон, JComponent Мӯҳтаво_қимат, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame равзана = new JFrame(равзана_Унвон);
        равзана.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        равзана.setContentPane(Мӯҳтаво_қимат);
        равзана.setSize(너비, 높이);
        равзана.setLocationByPlatform(true);
        равзана.setVisible(true);
        return равзана;
    }
}
