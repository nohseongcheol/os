// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Ranh giới native giới hạn của trình biên dịch, chỉ dành cho lệnh x86 và truy cập địa chỉ vật lý. */
public final class ThiếtBị {
    public static native int bộNhớTệp();
    public static native int góiGộpTệpJava();
    public static native int cỡGóiGộpTệpJava();
    public static native int đọcByteVàoRa(int sốHiệu);
    public static native void ghiByteVàoRa(int sốHiệu, int giáTrị);
    public static native int đọcBộNhớ(int địaChỉ);
    public static native void ghiBộNhớ(int địaChỉ, int giáTrị);
    public static native int dấuMốcKhởiĐộng();
    public static native int thôngTinKhởiĐộng();
    public static native int cáchDùngMảng();
    public static native void nhườngNgắn();
    public static native void việcThựcThiDừngHẳn();
    public static native void hoànThànhThử(int giáTrị);
    public static native int đọcSốNguyênVàoRa(int sốHiệu);
    public static native void ghiSốNguyênVàoRa(int sốHiệu, int giáTrị);
    public static native void ghiNgắnKiểuVàoRa(int sốHiệu, int giáTrị);
    public static native int đọcNgắnKiểuVàoRa(int sốHiệu);
    public static native void chuẩnBịChươngTrìnhNgườiDùng();
    public static native void cácNộiDungXóaSạchNgườiDùng();
    public static native int chạyChươngTrìnhNgườiDùng(int địaChỉMục, int địaChỉNgănXếpToánHạng);
    public static native int miliGiây();
    public static native int miliGiâyCònLạiNgườiDùng();
    public static native int GóiGộpTệpThựcThi();
    public static native int cỡGóiGộpTệpThựcThi();
    public static native int bộNhớMạng();
}
