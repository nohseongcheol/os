// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package English.Java;

import javax.swing.*;

public final class Screen {
    private Screen() {}
    public static void laterValue(Runnable action) { SwingUtilities.invokeLater(action); }
    /** Call on the Swing event dispatch thread. */
    public static JFrame window(String windowTitle, JComponent contentValue, int widthValue, int heightValue) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("Screen.laterValue 안에서 창을 만드세요");
        JFrame window = new JFrame(windowTitle);
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.setContentPane(contentValue);
        window.setSize(widthValue, heightValue);
        window.setLocationByPlatform(true);
        window.setVisible(true);
        return window;
    }
}
