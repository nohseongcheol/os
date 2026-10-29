// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable Aición) { SwingUtilities.invokeLater(Aición); }
    /** Swing 이벤트 처리 가닥에서 호출한다. */
    public static JFrame Ventana(String 제목, JComponent 내용, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame Ventana = new JFrame(제목);
        Ventana.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Ventana.setContentPane(내용);
        Ventana.setSize(너비, 높이);
        Ventana.setLocationByPlatform(true);
        Ventana.setVisible(true);
        return Ventana;
    }
}
