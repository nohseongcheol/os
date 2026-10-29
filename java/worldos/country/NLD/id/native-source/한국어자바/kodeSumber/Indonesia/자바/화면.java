// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Indonesia.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable Aksi) { SwingUtilities.invokeLater(Aksi); }
    /** Swing 이벤트 Proses_VALUE_entri 가닥에서 호출한다. */
    public static JFrame Jendela(String jendela_Judul, JComponent Isi_VALUE, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame Jendela = new JFrame(jendela_Judul);
        Jendela.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Jendela.setContentPane(Isi_VALUE);
        Jendela.setSize(너비, 높이);
        Jendela.setLocationByPlatform(true);
        Jendela.setVisible(true);
        return Jendela;
    }
}
