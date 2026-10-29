// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ελληνικά.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable Ενέργεια) { SwingUtilities.invokeLater(Ενέργεια); }
    /** Swing 이벤트 διεργασία_τιμή_καταχώρηση 가닥에서 호출한다. */
    public static JFrame Παράθυρο(String Παράθυρο_Τίτλος, JComponent Περιεχόμενο_τιμή, int 너비, int ύψος_τιμή) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame Παράθυρο = new JFrame(Παράθυρο_Τίτλος);
        Παράθυρο.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Παράθυρο.setContentPane(Περιεχόμενο_τιμή);
        Παράθυρο.setSize(너비, ύψος_τιμή);
        Παράθυρο.setLocationByPlatform(true);
        Παράθυρο.setVisible(true);
        return Παράθυρο;
    }
}
