// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Монгол.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable Үйлдэл) { SwingUtilities.invokeLater(Үйлдэл); }
    /** Swing 이벤트 үйл_явц_утга_оролт 가닥에서 호출한다. */
    public static JFrame цонх(String цонх_Гарчиг, JComponent Агуулга_утга, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame цонх = new JFrame(цонх_Гарчиг);
        цонх.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        цонх.setContentPane(Агуулга_утга);
        цонх.setSize(너비, 높이);
        цонх.setLocationByPlatform(true);
        цонх.setVisible(true);
        return цонх;
    }
}
