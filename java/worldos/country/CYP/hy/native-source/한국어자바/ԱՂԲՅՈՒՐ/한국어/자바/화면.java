// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable Գործողություն) { SwingUtilities.invokeLater(Գործողություն); }
    /** Swing 이벤트 Ընթացք_արժեք_մուտքագրում 가닥에서 호출한다. */
    public static JFrame պատուհան(String պատուհան_Անվանում, JComponent Բովանդակություն_արժեք, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame պատուհան = new JFrame(պատուհան_Անվանում);
        պատուհան.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        պատուհան.setContentPane(Բովանդակություն_արժեք);
        պատուհան.setSize(너비, 높이);
        պատուհան.setLocationByPlatform(true);
        պատուհան.setVisible(true);
        return պատուհան;
    }
}
