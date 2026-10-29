// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package українська.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable Дія) { SwingUtilities.invokeLater(Дія); }
    /** Swing 이벤트 процес_значення_запис 가닥에서 호출한다. */
    public static JFrame Вікно(String вікно_Назва, JComponent Вміст_значення, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame Вікно = new JFrame(вікно_Назва);
        Вікно.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Вікно.setContentPane(Вміст_значення);
        Вікно.setSize(너비, 높이);
        Вікно.setLocationByPlatform(true);
        Вікно.setVisible(true);
        return Вікно;
    }
}
