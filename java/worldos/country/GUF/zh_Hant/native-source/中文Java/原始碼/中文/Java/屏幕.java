// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.Java;

import javax.swing.*;

public final class 屏幕 {
    private 屏幕() {}
    public static void 稍後值(Runnable 動作) { SwingUtilities.invokeLater(動作); }
    /** 在 Swing 事件分派執行緒中呼叫。 */
    public static JFrame 窗口(String 窗口標題, JComponent 內容值, int 寬度值, int 高度值) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("屏幕.稍後值 안에서 창을 만드세요");
        JFrame 窗口 = new JFrame(窗口標題);
        窗口.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        窗口.setContentPane(內容值);
        窗口.setSize(寬度值, 高度值);
        窗口.setLocationByPlatform(true);
        窗口.setVisible(true);
        return 窗口;
    }
}
