// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable Аракети) { SwingUtilities.invokeLater(Аракети); }
    /** Swing 이벤트 Процесс_маани_киргизме_жазуу 가닥에서 호출한다. */
    public static JFrame терезе(String терезе_Наам, JComponent Мазмун_маани, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame терезе = new JFrame(терезе_Наам);
        терезе.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        терезе.setContentPane(Мазмун_маани);
        терезе.setSize(너비, 높이);
        терезе.setLocationByPlatform(true);
        терезе.setVisible(true);
        return терезе;
    }
}
