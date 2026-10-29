// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package العربية.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable إجراء) { SwingUtilities.invokeLater(إجراء); }
    /** Swing 이벤트 عملية_قيمة_إدخال 가닥에서 호출한다. */
    public static JFrame نافذة(String نافذة_عنوان, JComponent محتوى_قيمة, int 너비, int ارتفاع_قيمة) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame نافذة = new JFrame(نافذة_عنوان);
        نافذة.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        نافذة.setContentPane(محتوى_قيمة);
        نافذة.setSize(너비, ارتفاع_قيمة);
        نافذة.setLocationByPlatform(true);
        نافذة.setVisible(true);
        return نافذة;
    }
}
