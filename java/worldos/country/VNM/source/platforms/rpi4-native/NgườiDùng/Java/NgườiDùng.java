// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Cầu nối SVC dành cho công cụ Java ở ARM64 EL0. Được biên dịch cùng mã nguồn công cụ x86 hiện có. */
public final class NgườiDùng {
    public static native int mởBộMôTảTệp(int[] tên, int cácThiếtLập);
    public static native int đọcByteTệpMột(int mụcBộMôTả);
    public static native int ghiByteTệpMột(int mụcBộMôTả, int giáTrị);
    public static native int đóngBộMôTảTệp(int mụcBộMôTả);
    public static native int đọcTệp(int[] tên, int[] DữLiệu);
    public static native int ghiTệp(int[] tên, int[] DữLiệu, int độDài);
    public static native int ghi(String vănBản);
    public static native int ghiGiáTrịKýTự(int giáTrị);
    public static native int sốLượngCácĐốiSố();
    public static native String cácĐốiSố(int sốHiệu);
    public static native int sốCôngCụ();
    public static native int kếtNốiMànHình(int hànhĐộng, int sốHiệu, int toánHạngĐầuTiên, int toánHạngThứHai, int toánHạngThứBa, int toánHạngThứTư);
    public static native int vănBảnMànHình(int sốHiệu, int[] vănBản, int độDài);
    public static native int rộngMànHình();
    public static native int caoMànHình();
    public static native int điềuKhiểnLuồng(int hànhĐộng, int mụcBộMôTả, int giáTrị);
    public static native int kếtNốiLuồng(int mụcBộMôTả, int địaChỉ, int giáTrịCổng);
    public static native int mởMạng(int giáTrịCổng);
    public static native int gửiMạng(int mụcBộMôTả, int địaChỉ, int giáTrịCổng, int[] DữLiệu, int độDài);
    public static native int nhậnMạng(int mụcBộMôTả, int[] DữLiệu, int độDài);
    public static native int cổngMạng(int mụcBộMôTả);
    public static native int miliGiây();
    public static native int chờẢnhCho();
    public static native int hìnhChữNhật(int vịTríNgang, int vịTríDọc, int khoảngTrảiRộng, int giáTrịCao, int giáTrịMàu);
}
