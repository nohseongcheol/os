// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import javax.swing.*;

public final class 화면 {
    private 화면() {}
    public static void 나중에(Runnable ຄໍາສັ່ງ) { SwingUtilities.invokeLater(ຄໍາສັ່ງ); }
    /** Swing 이벤트 ຂະ_ບວນ_ການ_ຄ່າ_ເຂົ້າໃນ 가닥에서 호출한다. */
    public static JFrame ວິນໂດ(String ວິນໂດ_ຊື່, JComponent ເນື້ອໃນ_ຄ່າ_cb0f2404, int 너비, int 높이) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("화면.나중에 안에서 창을 만드세요");
        JFrame ວິນໂດ = new JFrame(ວິນໂດ_ຊື່);
        ວິນໂດ.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        ວິນໂດ.setContentPane(ເນື້ອໃນ_ຄ່າ_cb0f2404);
        ວິນໂດ.setSize(너비, 높이);
        ວິນໂດ.setLocationByPlatform(true);
        ວິນໂດ.setVisible(true);
        return ວິນໂດ;
    }
}
