// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Татарча.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable Гамәл) { SwingUtilities.invokeLater(Гамәл); }
    /** Swing 이벤트 Процесс_VALUE_кертү 가닥에서 호출한다. */
    public static JFrame тәрәз(String тәрәз_Башлам, JComponent Эчтәлек_VALUE, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame тәрәз = new JFrame(тәрәз_Башлам);
        тәрәз.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        тәрәз.setContentPane(Эчтәлек_VALUE);
        тәрәз.setSize(너비, 높이);
        тәрәз.setLocationByPlatform(true);
        тәрәз.setVisible(true);
        return тәрәз;
    }
}
