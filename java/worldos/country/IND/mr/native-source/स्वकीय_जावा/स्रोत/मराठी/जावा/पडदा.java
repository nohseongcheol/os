// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package मराठी.जावा;

import javax.swing.*;

public final class पडदा {
    private पडदा() {}
    public static void नंतर_मूल्य(Runnable कृती) { SwingUtilities.invokeLater(कृती); }
    /** Swing घटना-वितरण धाग्यावरून आवाहन करावे. */
    public static JFrame विंडो(String विंडो_शीर्षक, JComponent सामुग्री_मूल्य, int रुंदी_मूल्य, int उंची_मूल्य) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("पडदा.नंतर_मूल्य 안에서 창을 만드세요");
        JFrame विंडो = new JFrame(विंडो_शीर्षक);
        विंडो.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        विंडो.setContentPane(सामुग्री_मूल्य);
        विंडो.setSize(रुंदी_मूल्य, उंची_मूल्य);
        विंडो.setLocationByPlatform(true);
        विंडो.setVisible(true);
        return विंडो;
    }
}
