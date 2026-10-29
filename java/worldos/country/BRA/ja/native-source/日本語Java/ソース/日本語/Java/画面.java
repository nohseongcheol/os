// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 日本語.Java;

import javax.swing.*;

public final class 画面 {
    private 画面() {}
    public static void 後続値(Runnable 動作) { SwingUtilities.invokeLater(動作); }
    /** Swing の事象処理スレッドから呼び出す。 */
    public static JFrame 窓(String 窓表題, JComponent 内容物値, int 幅値, int 高さ値) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("画面.後続値 안에서 창을 만드세요");
        JFrame 窓 = new JFrame(窓表題);
        窓.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        窓.setContentPane(内容物値);
        窓.setSize(幅値, 高さ値);
        窓.setLocationByPlatform(true);
        窓.setVisible(true);
        return 窓;
    }
}
