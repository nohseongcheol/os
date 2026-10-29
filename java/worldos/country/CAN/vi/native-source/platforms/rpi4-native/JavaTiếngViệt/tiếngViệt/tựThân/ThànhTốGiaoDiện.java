// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package tiếngViệt.tựThân;
/** Hàm tiện ích tạo thành phần màn hình của API tiếng Việt. */
public final class ThànhTốGiaoDiện {
    private ThànhTốGiaoDiện() {}
    public static void gọiThựcHiệnVềSau(TácVụChạyĐược HànhĐộngTácVụ) { HàngĐợiSựKiện.gọiThựcHiệnVềSau(HànhĐộngTácVụ); }
    public static nhãn giáTrịThẻ(String vănBản, int vịTríNgang, int vịTríDọc, int khoảngTrảiRộng, int giáTrịCao) {
        return new nhãn(vănBản, vịTríNgang, vịTríDọc, khoảngTrảiRộng, giáTrịCao);
    }
    public static nút nút(String vănBản, int vịTríNgang, int vịTríDọc, int khoảngTrảiRộng, int giáTrịCao, BộNhậnHànhĐộng giáTrịBộNhận) {
        return new nút(vănBản, vịTríNgang, vịTríDọc, khoảngTrảiRộng, giáTrịCao, giáTrịBộNhận);
    }
    public static TrườngVănBản TrườngVănBản(String vănBản, int vịTríNgang, int vịTríDọc, int khoảngTrảiRộng, int giáTrịCao) {
        return new TrườngVănBản(vănBản, vịTríNgang, vịTríDọc, khoảngTrảiRộng, giáTrịCao);
    }
}
