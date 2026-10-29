// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable mmèm) { SwingUtilities.invokeLater(mmèm); }
    /** Swing 이벤트 ùsòrò_valuu_ndebà 가닥에서 호출한다. */
    public static JFrame windò(String windò_Isi_okwu, JComponent ndịnà_valuu, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame windò = new JFrame(windò_Isi_okwu);
        windò.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        windò.setContentPane(ndịnà_valuu);
        windò.setSize(너비, 높이);
        windò.setLocationByPlatform(true);
        windò.setVisible(true);
        return windò;
    }
}
