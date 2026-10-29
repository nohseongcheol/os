// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ಕನ್ನಡ.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable ಹಕ್ರಿಯೆ) { SwingUtilities.invokeLater(ಹಕ್ರಿಯೆ); }
    /** Swing 이벤트 ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ_ನಮೂದು 가닥에서 호출한다. */
    public static JFrame ವಿಂಡೋ(String ವಿಂಡೋ_ಶೀರ್ಷಿಕೆ, JComponent ವಿಷಯ_ಮೌಲ್ಯ, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame ವಿಂಡೋ = new JFrame(ವಿಂಡೋ_ಶೀರ್ಷಿಕೆ);
        ವಿಂಡೋ.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        ವಿಂಡೋ.setContentPane(ವಿಷಯ_ಮೌಲ್ಯ);
        ವಿಂಡೋ.setSize(너비, 높이);
        ವಿಂಡೋ.setLocationByPlatform(true);
        ವಿಂಡೋ.setVisible(true);
        return ವಿಂಡೋ;
    }
}
