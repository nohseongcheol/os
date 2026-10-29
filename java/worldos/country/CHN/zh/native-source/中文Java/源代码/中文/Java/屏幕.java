// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.Java;

import javax.swing.*;

public final class 屏幕 {
    private 屏幕() {}
    public static void 稍后值(Runnable 动作) { SwingUtilities.invokeLater(动作); }
    /** 在 Swing 事件分派线程中调用。 */
    public static JFrame 窗口(String 窗口标题, JComponent 内容值, int 宽度值, int 高度值) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("屏幕.稍后值 안에서 창을 만드세요");
        JFrame 窗口 = new JFrame(窗口标题);
        窗口.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        窗口.setContentPane(内容值);
        窗口.setSize(宽度值, 高度值);
        窗口.setLocationByPlatform(true);
        窗口.setVisible(true);
        return 窗口;
    }
}
