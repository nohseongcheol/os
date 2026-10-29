// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable कृती) { SwingUtilities.invokeLater(कृती); }
    /** Swing 이벤트 प्रक्रिया_मोल_प्रवेश 가닥에서 호출한다. */
    public static JFrame विंडो(String विंडो_शीर्षक, JComponent अनुक्रमणिका_मोल, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame विंडो = new JFrame(विंडो_शीर्षक);
        विंडो.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        विंडो.setContentPane(अनुक्रमणिका_मोल);
        विंडो.setSize(너비, 높이);
        विंडो.setLocationByPlatform(true);
        विंडो.setVisible(true);
        return विंडो;
    }
}
