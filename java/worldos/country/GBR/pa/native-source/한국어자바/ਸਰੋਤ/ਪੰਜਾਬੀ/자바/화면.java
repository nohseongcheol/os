// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ਪੰਜਾਬੀ.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable ਐਕਸ਼ਨ) { SwingUtilities.invokeLater(ਐਕਸ਼ਨ); }
    /** Swing 이벤트 ਕਾਰਵਾਈ_ਕੀਮਤ_ਦਾਖਲਾ 가닥에서 호출한다. */
    public static JFrame ਵਿੰਡੋ(String ਵਿੰਡੋ_ਸਿਰਲੇਖ, JComponent ਤਤਕਰਾ_ਕੀਮਤ, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame ਵਿੰਡੋ = new JFrame(ਵਿੰਡੋ_ਸਿਰਲੇਖ);
        ਵਿੰਡੋ.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        ਵਿੰਡੋ.setContentPane(ਤਤਕਰਾ_ਕੀਮਤ);
        ਵਿੰਡੋ.setSize(너비, 높이);
        ਵਿੰਡੋ.setLocationByPlatform(true);
        ਵਿੰਡੋ.setVisible(true);
        return ਵਿੰਡੋ;
    }
}
