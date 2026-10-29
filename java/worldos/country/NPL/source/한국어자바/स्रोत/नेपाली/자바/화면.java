// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package नेपाली.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable कार्य) { SwingUtilities.invokeLater(कार्य); }
    /** Swing 이벤트 प्रक्रिया_मान_प्रविष्टि 가닥에서 호출한다. */
    public static JFrame सन्झ्याल(String सन्झ्याल_शिर्षक, JComponent सामग्री_मान, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame सन्झ्याल = new JFrame(सन्झ्याल_शिर्षक);
        सन्झ्याल.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        सन्झ्याल.setContentPane(सामग्री_मान);
        सन्झ्याल.setSize(너비, 높이);
        सन्झ्याल.setLocationByPlatform(true);
        सन्झ्याल.setVisible(true);
        return सन्झ्याल;
    }
}
