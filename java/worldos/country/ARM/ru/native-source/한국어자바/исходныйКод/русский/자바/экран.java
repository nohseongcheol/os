// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package русский.자바;

import javax.swing.*;

public final class экран {
    private экран() {}
    public static void 나중에(Runnable Действие) { SwingUtilities.invokeLater(Действие); }
    /** Swing 이벤트 Процесс_ЗНАЧЕН_ввод 가닥에서 호출한다. */
    public static JFrame Окно(String окно_право, JComponent контент_ЗНАЧЕН, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("экран.나중에 안에서 창을 만드세요");
        JFrame Окно = new JFrame(окно_право);
        Окно.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Окно.setContentPane(контент_ЗНАЧЕН);
        Окно.setSize(너비, 높이);
        Окно.setLocationByPlatform(true);
        Окно.setVisible(true);
        return Окно;
    }
}
