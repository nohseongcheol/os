// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable ᎠᏛᏁᎵᏓ) { SwingUtilities.invokeLater(ᎠᏛᏁᎵᏓ); }
    /** Swing 이벤트 ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ 가닥에서 호출한다. */
    public static JFrame ᏦᎳᏂ(String 제목, JComponent ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame ᏦᎳᏂ = new JFrame(제목);
        ᏦᎳᏂ.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        ᏦᎳᏂ.setContentPane(ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ);
        ᏦᎳᏂ.setSize(너비, 높이);
        ᏦᎳᏂ.setLocationByPlatform(true);
        ᏦᎳᏂ.setVisible(true);
        return ᏦᎳᏂ;
    }
}
