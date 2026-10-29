// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package tiếngViệt.tựThân;
/** Cửa sổ nối trực tiếp với JVM tự xây dựng và bộ quản lý cửa sổ của nhân. */
public final class cửaSổ extends PhầnTửMànHình {
    public cửaSổ(String tiêuĐềCửaSổ, int khoảngTrảiRộng, int giáTrịCao) {
        throw new NgoạiLệTrạngThái("JVM riêng phải hỗ trợ tạo cửa sổ qua API tiếng Việt.");
    }
    public native void thêmPhầnTử(PhầnTửMànHình giáTrịPhầnTử);
    public native void hiệnCửaSổ();
    public native void đóng();
    public native boolean làHiệnĐược();
}
