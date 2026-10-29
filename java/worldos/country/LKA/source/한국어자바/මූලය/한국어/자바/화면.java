// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable ක්_රීයාව) { SwingUtilities.invokeLater(ක්_රීයාව); }
    /** Swing 이벤트 ක්_රියාවලිය_අගය_පිවිසුම 가닥에서 호출한다. */
    public static JFrame කවුළුව(String කවුළුව_මාතෘකාව, JComponent අන්තර්ගතය_අගය, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame කවුළුව = new JFrame(කවුළුව_මාතෘකාව);
        කවුළුව.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        කවුළුව.setContentPane(අන්තර්ගතය_අගය);
        කවුළුව.setSize(너비, 높이);
        කවුළුව.setLocationByPlatform(true);
        කවුළුව.setVisible(true);
        return කවුළුව;
    }
}
