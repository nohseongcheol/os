// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable کم) { SwingUtilities.invokeLater(کم); }
    /** Swing 이벤트 عمل_قدر_داخلہ 가닥에서 호출한다. */
    public static JFrame کھڑکی(String کھڑکی_عنوان, JComponent اجزاء_قدر, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame کھڑکی = new JFrame(کھڑکی_عنوان);
        کھڑکی.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        کھڑکی.setContentPane(اجزاء_قدر);
        کھڑکی.setSize(너비, 높이);
        کھڑکی.setLocationByPlatform(true);
        کھڑکی.setVisible(true);
        return کھڑکی;
    }
}
