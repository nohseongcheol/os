// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Türkçe.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable Eylem) { SwingUtilities.invokeLater(Eylem); }
    /** Swing 이벤트 işlem_değer_girdi 가닥에서 호출한다. */
    public static JFrame Pencere(String pencere_Başlık, JComponent içerik_değer, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame Pencere = new JFrame(pencere_Başlık);
        Pencere.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Pencere.setContentPane(içerik_değer);
        Pencere.setSize(너비, 높이);
        Pencere.setLocationByPlatform(true);
        Pencere.setVisible(true);
        return Pencere;
    }
}
