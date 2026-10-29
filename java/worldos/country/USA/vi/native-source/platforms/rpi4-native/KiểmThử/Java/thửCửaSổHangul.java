// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import tiếngViệt.tựThân.cửaSổ;
import tiếngViệt.tựThân.ThànhTốGiaoDiện;
import tiếngViệt.tựThân.*;

public class thửCửaSổHangul implements TácVụChạyĐược, BộNhậnHànhĐộng {
    cửaSổ MànHình;
    nhãn HướngDẫn;
    TrườngVănBản giáTrịVào;
    public void thựcThiTácVụ() {
        CácPhépKiểmTra.đòiHỏi(HàngĐợiSựKiện.làĐangĐiềuPhốiSựKiện(), "tiếngViệt MànHình TácVụ 큐");
        MànHình = new cửaSổ("tiếngViệt thưViện cửaSổ", 400, 280);
        HướngDẫn = ThànhTốGiaoDiện.giáTrịThẻ("한글로 Java 코딩", 20, 20, 340, 30);
        giáTrịVào = ThànhTốGiaoDiện.TrườngVănBản("tên", 20, 65, 340, 30);
        MànHình.thêmPhầnTử(HướngDẫn);
        MànHình.thêmPhầnTử(giáTrịVào);
        MànHình.thêmPhầnTử(ThànhTốGiaoDiện.nút("chào", 20, 110, 180, 32, this));
        MànHình.hiệnCửaSổ();
        ĐầuRa.ghiDòng("KOREAN SWING READY");
    }
    public void nhậnHànhĐộng(ThôngBáoHànhĐộng sựKiện) {
        CácPhépKiểmTra.đòiHỏi(HàngĐợiSựKiện.làĐangĐiềuPhốiSựKiện(), "tiếngViệt hànhĐộng 되부름");
        CácPhépKiểmTra.đòiHỏi(sựKiện.sốHiệu() == 1001 && sựKiện.nguồnSựKiện() instanceof nút, "tiếngViệt sựKiện 객체와 giáTrịGốc");
        CácPhépKiểmTra.đòiHỏi(!((Object)sựKiện.nguồnSựKiện() instanceof javax.swing.JButton), "표준 단추와 독립된 giáTrịĐịnhDạng");
        CácPhépKiểmTra.đòiHỏi(!((Object)sựKiện instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 giáTrịĐịnhDạng");
        HướngDẫn.ghiVănBản("안녕하세요 " + giáTrịVào.đọcVănBản());
        ĐầuRa.ghiDòng("KOREAN SWING CLICK " + giáTrịVào.đọcVănBản());
    }
    public static void main(String[] cácĐốiSố) {
        HàngĐợiSựKiện.gọiThựcHiệnVềSau(new thửCửaSổHangul());
    }
}
