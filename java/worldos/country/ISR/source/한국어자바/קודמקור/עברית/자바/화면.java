// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package עברית.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable פעולה) { SwingUtilities.invokeLater(פעולה); }
    /** Swing 이벤트 תהליך_ערך_ערך 가닥에서 호출한다. */
    public static JFrame חלון(String חלון_כותר, JComponent תוכן_ערך, int 너비, int גובה_ערך) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame חלון = new JFrame(חלון_כותר);
        חלון.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        חלון.setContentPane(תוכן_ערך);
        חלון.setSize(너비, גובה_ערך);
        חלון.setLocationByPlatform(true);
        חלון.setVisible(true);
        return חלון;
    }
}
