// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Български.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable Операция) { SwingUtilities.invokeLater(Операция); }
    /** Swing 이벤트 Процес_стойност_запис 가닥에서 호출한다. */
    public static JFrame Прозорец(String прозорец_Заглавие, JComponent Съдържание_стойност, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame Прозорец = new JFrame(прозорец_Заглавие);
        Прозорец.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Прозорец.setContentPane(Съдържание_стойност);
        Прозорец.setSize(너비, 높이);
        Прозорец.setLocationByPlatform(true);
        Прозорец.setVisible(true);
        return Прозорец;
    }
}
