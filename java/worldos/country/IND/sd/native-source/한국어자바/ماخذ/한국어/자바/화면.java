// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable عمل) { SwingUtilities.invokeLater(عمل); }
    /** Swing 이벤트 عمل_قدر_داخلا 가닥에서 호출한다. */
    public static JFrame دري(String دري_عنوان, JComponent مواد_قدر, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame دري = new JFrame(دري_عنوان);
        دري.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        دري.setContentPane(مواد_قدر);
        دري.setSize(너비, 높이);
        دري.setLocationByPlatform(true);
        دري.setVisible(true);
        return دري;
    }
}
