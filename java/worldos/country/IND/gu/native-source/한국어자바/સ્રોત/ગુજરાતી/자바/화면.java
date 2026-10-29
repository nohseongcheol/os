// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ગુજરાતી.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable ક્રિયા) { SwingUtilities.invokeLater(ક્રિયા); }
    /** Swing 이벤트 પ્રક્રિયા_મૂલ્ય_પ્રવેશ 가닥에서 호출한다. */
    public static JFrame વિંડો(String વિંડો_શીર્ષક, JComponent સામગ્રી_મૂલ્ય, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame વિંડો = new JFrame(વિંડો_શીર્ષક);
        વિંડો.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        વિંડો.setContentPane(સામગ્રી_મૂલ્ય);
        વિંડો.setSize(너비, 높이);
        વિંડો.setLocationByPlatform(true);
        વિંડો.setVisible(true);
        return વિંડો;
    }
}
