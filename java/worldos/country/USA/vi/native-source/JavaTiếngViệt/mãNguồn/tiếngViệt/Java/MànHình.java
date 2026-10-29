// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package tiếngViệt.Java;

import javax.swing.*;

public final class MànHình {
    private MànHình() {}
    public static void giáTrịVềSau(Runnable hànhĐộng) { SwingUtilities.invokeLater(hànhĐộng); }
    /** Gọi trên luồng phân phối sự kiện của Swing. */
    public static JFrame cửaSổ(String tiêuĐềCửaSổ, JComponent giáTrịNộiDung, int giáTrịRộng, int giáTrịCao) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("MànHình.giáTrịVềSau 안에서 창을 만드세요");
        JFrame cửaSổ = new JFrame(tiêuĐềCửaSổ);
        cửaSổ.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        cửaSổ.setContentPane(giáTrịNộiDung);
        cửaSổ.setSize(giáTrịRộng, giáTrịCao);
        cửaSổ.setLocationByPlatform(true);
        cửaSổ.setVisible(true);
        return cửaSổ;
    }
}
