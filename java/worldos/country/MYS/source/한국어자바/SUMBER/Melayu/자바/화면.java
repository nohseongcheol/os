// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Melayu.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable Aksi) { SwingUtilities.invokeLater(Aksi); }
    /** Swing 이벤트 Proses_VALUE_pemasukan 가닥에서 호출한다. */
    public static JFrame Tetingkap(String tetingkap_Tajuk, JComponent Kandungan_VALUE, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame Tetingkap = new JFrame(tetingkap_Tajuk);
        Tetingkap.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Tetingkap.setContentPane(Kandungan_VALUE);
        Tetingkap.setSize(너비, 높이);
        Tetingkap.setLocationByPlatform(true);
        Tetingkap.setVisible(true);
        return Tetingkap;
    }
}
