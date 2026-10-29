// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Ranh giới máy ARM64. Không cắt con trỏ thành int của Java. */
public final class BoMạch {
    public static native int đọcĐiểmẢnhHiểnThị(int vịTríNgang, int vịTríDọc);
    public static native void ghiĐiểmẢnhHiểnThị(int vịTríNgang, int vịTríDọc, int giáTrịMàu);
    public static native int điềuKhiểnTừXa(int giáTrịLoại, int hànhĐộng);
    public static native void lệnhTừXaKếtThúc(int giáTrịTrạngThái);
    public static native void chờTừXa(int giáTrịTrạngThái);
    public static native void ghiNốiTiếp(int giáTrị);
    public static native int đọcNốiTiếp();
    public static native int miliGiây();
    public static native int mứcĐặcQuyềnCPU();
    public static native int chuẩnBịMànHình();
    public static native int rộngMànHình();
    public static native int caoMànHình();
    public static native void đặtĐiểmẢnhMànHình(int vịTríNgang, int vịTríDọc, int giáTrịMàu);
    public static native void nhườngBộXửLýTrungTâm();
    public static native int tạoTácVụ(int sốHiệu);
    public static native int trạngTháiTácVụ(int sốHiệu);
    public static native void dừng(int giáTrịTrạngThái);
    public static native int thửCộngCộng();
    public static native int chạyChươngTrìnhNgườiDùng(int sốHiệu);
    public static native int kiểmTraChươngTrìnhNgườiDùng();
    public static native int chuẩnBịCácĐốiSố(int sốLượngPhầnMục);
    public static native int thựcThiTệpNgườiDùng();
    public static native int thựcThiTệpLinux();
    public static native int byteĐốiSố(int sốHiệu, int vịTrí, int giáTrị);
    public static native int thiếtBịCuối(int hànhĐộng);
    public static native int chươngTrìnhNgườiDùngĐiềuKhiển(int hànhĐộng);
    public static native void vàoRaChuyển(int hànhĐộng);
    public static native int dịchVụChuyểnGiaoTệp(int hànhĐộng);
    public static native int tìnhTrạngMạng(int giáTrịMục, int sốHiệu);
    public static native int cácThiếtLậpMạng(int hànhĐộng, int địaChỉ, int giáTrịMặtNạ, int giáTrịCổngNối);
    public static native int gửiPhảnHồi(int địaChỉ, int giáTrịThứTự);
    public static native int đọcPhảnHồi(int giáTrịMục);
    public static native int hệThốngTruyVấn(int giáTrịMục, int sốHiệu);
    public static native void tắtNguồnĐiện();
}
