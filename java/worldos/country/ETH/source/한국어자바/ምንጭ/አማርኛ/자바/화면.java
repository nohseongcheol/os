// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package አማርኛ.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable ተግባር) { SwingUtilities.invokeLater(ተግባር); }
    /** Swing 이벤트 ሂደት_እሴት_ምዝግብ 가닥에서 호출한다. */
    public static JFrame መስኮት(String መስኮት_ርዕስ, JComponent ይዘት_እሴት, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame መስኮት = new JFrame(መስኮት_ርዕስ);
        መስኮት.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        መስኮት.setContentPane(ይዘት_እሴት);
        መስኮት.setSize(너비, 높이);
        መስኮት.setLocationByPlatform(true);
        መስኮት.setVisible(true);
        return መስኮት;
    }
}
