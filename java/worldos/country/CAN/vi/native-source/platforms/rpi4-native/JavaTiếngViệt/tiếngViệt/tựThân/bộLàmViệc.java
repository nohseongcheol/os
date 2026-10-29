// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package tiếngViệt.tựThân;
/** Dòng thực thi do bộ lập lịch của JVM tự xây dựng quản lý; không bọc Thread tiêu chuẩn. */
public final class bộLàmViệc {
    public bộLàmViệc(TácVụChạyĐược HànhĐộngTácVụ) {
        throw new NgoạiLệTrạngThái("JVM riêng phải hỗ trợ tạo luồng qua API tiếng Việt.");
    }
    public native void bắtChạyTácVụ() throws NgoạiLệTrạngTháiLuồngChạy;
    public native void đợi() throws NgoạiLệĐãBịNgắtChờ;
    public native boolean làCònSống();
    public static native void nhườngTácVụ();
}
