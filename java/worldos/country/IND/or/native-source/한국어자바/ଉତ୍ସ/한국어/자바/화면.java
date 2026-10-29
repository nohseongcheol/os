// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable କାମ) { SwingUtilities.invokeLater(କାମ); }
    /** Swing 이벤트 ପ୍ରୋସେସ୍_ମୂଲ୍ୟ_ଏଣ୍ଟ୍ରି 가닥에서 호출한다. */
    public static JFrame ଓ୍ୱିଣ୍ଡୋ(String ଓ୍ୱିଣ୍ଡୋ_ଟାଇଟେଲ୍, JComponent ବିଷୟ_ମୂଲ୍ୟ, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame ଓ୍ୱିଣ୍ଡୋ = new JFrame(ଓ୍ୱିଣ୍ଡୋ_ଟାଇଟେଲ୍);
        ଓ୍ୱିଣ୍ଡୋ.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        ଓ୍ୱିଣ୍ଡୋ.setContentPane(ବିଷୟ_ମୂଲ୍ୟ);
        ଓ୍ୱିଣ୍ଡୋ.setSize(너비, 높이);
        ଓ୍ୱିଣ୍ଡୋ.setLocationByPlatform(true);
        ଓ୍ୱିଣ୍ଡୋ.setVisible(true);
        return ଓ୍ୱିଣ୍ଡୋ;
    }
}
