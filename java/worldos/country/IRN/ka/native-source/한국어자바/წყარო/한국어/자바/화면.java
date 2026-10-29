// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable ქმედება) { SwingUtilities.invokeLater(ქმედება); }
    /** Swing 이벤트 პროცესი_მნიშვნელობა_შენატანი 가닥에서 호출한다. */
    public static JFrame ფანჯარა(String ფანჯარა_დასახელება, JComponent შიგთავსი_მნიშვნელობა, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame ფანჯარა = new JFrame(ფანჯარა_დასახელება);
        ფანჯარა.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        ფანჯარა.setContentPane(შიგთავსი_მნიშვნელობა);
        ფანჯარა.setSize(너비, 높이);
        ფანჯარა.setLocationByPlatform(true);
        ფანჯარა.setVisible(true);
        return ფანჯარა;
    }
}
