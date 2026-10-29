// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package हिंदी.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable क्रिया) { SwingUtilities.invokeLater(क्रिया); }
    /** Swing 이벤트 प्रक्रिया_मान_एन्ट्री 가닥에서 호출한다. */
    public static JFrame खिड़की(String विंडो_शीर्षक, JComponent सामग्री_मान, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame खिड़की = new JFrame(विंडो_शीर्षक);
        खिड़की.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        खिड़की.setContentPane(सामग्री_मान);
        खिड़की.setSize(너비, 높이);
        खिड़की.setLocationByPlatform(true);
        खिड़की.setVisible(true);
        return खिड़की;
    }
}
