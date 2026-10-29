// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package বাংলা.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable কাজ) { SwingUtilities.invokeLater(কাজ); }
    /** Swing 이벤트 প্রসেসর_মান_ভুক্তি 가닥에서 호출한다. */
    public static JFrame উইন্ডো(String উইন্ডো_শিরোনাম, JComponent সামগ্রি_মান, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame উইন্ডো = new JFrame(উইন্ডো_শিরোনাম);
        উইন্ডো.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        উইন্ডো.setContentPane(সামগ্রি_মান);
        উইন্ডো.setSize(너비, 높이);
        উইন্ডো.setLocationByPlatform(true);
        উইন্ডো.setVisible(true);
        return উইন্ডো;
    }
}
