// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package தமிழ்.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable செயல்) { SwingUtilities.invokeLater(செயல்); }
    /** Swing 이벤트 செயலகம்_மதிப்பு_உள்ளீடு 가닥에서 호출한다. */
    public static JFrame சாளரம்(String சாளரம்_தலைப்பு, JComponent உள்ளடக்கம்_மதிப்பு, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame சாளரம் = new JFrame(சாளரம்_தலைப்பு);
        சாளரம்.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        சாளரம்.setContentPane(உள்ளடக்கம்_மதிப்பு);
        சாளரம்.setSize(너비, 높이);
        சாளரம்.setLocationByPlatform(true);
        சாளரம்.setVisible(true);
        return சாளரம்;
    }
}
