// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable អំពើ) { SwingUtilities.invokeLater(អំពើ); }
    /** Swing 이벤트 ដំណើរការ_តំលៃ_ការបញ្ចូល 가닥에서 호출한다. */
    public static JFrame វីនដូ(String វីនដូ_ចំណងជើង, JComponent មាតិកា_តំលៃ, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame វីនដូ = new JFrame(វីនដូ_ចំណងជើង);
        វីនដូ.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        វីនដូ.setContentPane(មាតិកា_តំលៃ);
        វីនដូ.setSize(너비, 높이);
        វីនដូ.setLocationByPlatform(true);
        វីនដូ.setVisible(true);
        return វីនដូ;
    }
}
