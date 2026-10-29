// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package اردو.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable عمل) { SwingUtilities.invokeLater(عمل); }
    /** Swing 이벤트 عمل_قدر_اندراج 가닥에서 호출한다. */
    public static JFrame ونڈو(String دریچہ_عنوان, JComponent مشمول_قدر, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame ونڈو = new JFrame(دریچہ_عنوان);
        ونڈو.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        ونڈو.setContentPane(مشمول_قدر);
        ونڈو.setSize(너비, 높이);
        ونڈو.setLocationByPlatform(true);
        ونڈو.setVisible(true);
        return ونڈو;
    }
}
