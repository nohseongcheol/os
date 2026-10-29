// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** API dành riêng cho ELF người dùng của jkoros; không phải JNI cho Linux/JVM hay java.net. */
public final class NgườiDùng {
    public static native int mởBộMôTảTệp(int[] tênMụcTệp, int mởCácThiếtLập);
    public static native int đọcByteTệpMột(int bộMôTảTệp);
    public static native int ghiByteTệpMột(int bộMôTảTệp, int giáTrịByte);
    public static native int đóngBộMôTảTệp(int bộMôTảTệp);
    public static native int lưuTrữTệpChốt(int bộMôTảTệp);
    public static native int đọcTệp(int[] tên, int[] DữLiệu);
    public static native int ghiGiáTrịKýTự(int KýTự);
    public static native int ghiTệp(int[] tên, int[] DữLiệu, int độDài);
    public static native int ghi(String giáTrịNộiDung);
    public static native int sốLượngCácĐốiSố();
    public static native String cácĐốiSố(int sốHiệu);
    public static native int quyềnViệcThựcThi();
    public static native int mởMạng(int cổngCụcBộ);
    public static native int gửiDữLiệu(int giáTrịThẻXửLý, int địaChỉ, int cổngĐích, int[] DữLiệu, int độDài);
    public static native int nhậnDữLiệu(int giáTrịThẻXửLý, int[] DữLiệu, int miliGiâyGiớiHạn);
    public static native int đóngMạng(int giáTrịThẻXửLý);
    public static native int địaChỉTựCó();
    public static native int địaChỉĐãGửi(int giáTrịThẻXửLý);
    public static native int cổngĐãGửi(int giáTrịThẻXửLý);
}
