// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package tiếngViệt.tựThân;
/** Luồng là một dòng thực thi. JVM tự xây dựng luân phiên các luồng theo số lệnh đã chạy. */
public final class TácVụ {
    private TácVụ() {}
    public static bộLàmViệc chạy(TácVụChạyĐược HànhĐộngTácVụ) { bộLàmViệc giáTrịLuồngChạy = new bộLàmViệc(HànhĐộngTácVụ); giáTrịLuồngChạy.bắtChạyTácVụ(); return giáTrịLuồngChạy; }
    public static void đợi(bộLàmViệc giáTrịLuồngChạy) throws NgoạiLệĐãBịNgắtChờ { giáTrịLuồngChạy.đợi(); }
    public static boolean làCònSống(bộLàmViệc giáTrịLuồngChạy) { return giáTrịLuồngChạy.làCònSống(); }
    public static void nhườngTácVụ() { bộLàmViệc.nhườngTácVụ(); }
}
