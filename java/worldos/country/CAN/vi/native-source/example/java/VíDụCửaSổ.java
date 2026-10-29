// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import tiếngViệt.tựThân.cửaSổ;
import tiếngViệt.tựThân.nhãn;
import tiếngViệt.tựThân.TrườngVănBản;
import tiếngViệt.tựThân.nút;
import tiếngViệt.tựThân.HàngĐợiSựKiện;
import tiếngViệt.tựThân.ĐầuRa;
import tiếngViệt.tựThân.TácVụChạyĐược;
import tiếngViệt.tựThân.BộNhậnHànhĐộng;
import tiếngViệt.tựThân.ThôngBáoHànhĐộng;

/** Cửa sổ Swing trên nhân độc lập: nhập tiếng Việt, bấm nút rồi cập nhật nhãn thông báo. */
public class VíDụCửaSổ implements TácVụChạyĐược, BộNhậnHànhĐộng {
    private cửaSổ cửaSổLờiChào;
    private TrườngVănBản trườngTên;
    private nhãn lờiChào;
    private int sốLượngLờiChào;

    public void mởCửaSổ() {
        cửaSổLờiChào = new cửaSổ("vi Swing", 460, 300);
        cửaSổLờiChào.thêmPhầnTử(new nhãn("Xin chào", 20, 20, 420, 28));
        trườngTên = new TrườngVănBản("vi", 20, 64, 420, 30);
        lờiChào = new nhãn("Xin chào", 20, 152, 420, 28);
        cửaSổLờiChào.thêmPhầnTử(trườngTên);
        cửaSổLờiChào.thêmPhầnTử(new nút("chào", 20, 108, 180, 32, this));
        cửaSổLờiChào.thêmPhầnTử(lờiChào);
        cửaSổLờiChào.thêmPhầnTử(new nhãn("F9 / Shift+Space | X", 20, 204, 420, 28));
        cửaSổLờiChào.hiệnCửaSổ();
        ĐầuRa.ghiDòng("GUI VíDụ chuẩnBị: VíDụCửaSổ");
    }

    public void chào() {
        sốLượngLờiChào++;
        lờiChào.ghiVănBản("Xin chào, " + trườngTên.đọcVănBản() + "님! (" + sốLượngLờiChào + ")");
        ĐầuRa.ghiDòng("GUI LờiChào: " + lờiChào.đọcVănBản());
    }

    public void thựcThiTácVụ() { mởCửaSổ(); }
    public void nhậnHànhĐộng(ThôngBáoHànhĐộng thôngBáo) {
        ĐầuRa.ghiDòng("hànhĐộng thôngBáo: " + thôngBáo.vănBảnLệnh());
        chào();
    }
    public static void chạy() {
        HàngĐợiSựKiện.gọiThựcHiệnVềSau(new VíDụCửaSổ());
    }
}
