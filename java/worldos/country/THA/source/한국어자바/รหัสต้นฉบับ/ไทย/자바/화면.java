// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ไทย.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable การกระทํา) { SwingUtilities.invokeLater(การกระทํา); }
    /** Swing 이벤트 กระบวนการ_ค่า_รายการ 가닥에서 호출한다. */
    public static JFrame หน้าต่าง(String หน้าต่าง_กรรมสิทธิ์, JComponent เนื้อหา_ค่า, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame หน้าต่าง = new JFrame(หน้าต่าง_กรรมสิทธิ์);
        หน้าต่าง.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        หน้าต่าง.setContentPane(เนื้อหา_ค่า);
        หน้าต่าง.setSize(너비, 높이);
        หน้าต่าง.setLocationByPlatform(true);
        หน้าต่าง.setVisible(true);
        return หน้าต่าง;
    }
}
