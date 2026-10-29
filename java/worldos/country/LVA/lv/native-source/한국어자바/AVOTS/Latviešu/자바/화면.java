// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latviešu.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable Darbība) { SwingUtilities.invokeLater(Darbība); }
    /** Swing 이벤트 Process_VALUE_ievade 가닥에서 호출한다. */
    public static JFrame Logs(String logs_nosaukums, JComponent Saturs_VALUE, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame Logs = new JFrame(logs_nosaukums);
        Logs.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Logs.setContentPane(Saturs_VALUE);
        Logs.setSize(너비, 높이);
        Logs.setLocationByPlatform(true);
        Logs.setVisible(true);
        return Logs;
    }
}
