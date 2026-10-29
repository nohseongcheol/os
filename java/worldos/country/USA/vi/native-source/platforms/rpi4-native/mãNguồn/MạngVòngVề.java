// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Lớp mạng ban đầu: truyền IPv4/UDP vòng về trong một nhân. IP bên ngoài trả ENETUNREACH; không thay thế trình điều khiển gói Ethernet/IP. Có 8 điểm cuối, mỗi điểm giữ 4 thông điệp, mỗi thông điệp 512 byte. Mọi lời gọi đều không chặn. */
public final class MạngVòngVề {
    static int[] giáTrịDùng = new int[8];
    static int[] giáTrịCổng = new int[8];
    static int[] địaChỉ = new int[8];
    static int[] giáTrịPhíaTrước = new int[8];
    static int[] sốLượngPhầnMục = new int[8];
    static int[] cổngĐãNhận = new int[8];
    static int[] độDài = new int[32];
    static int[] cổngĐãGửi = new int[32];
    static int[] DữLiệu = new int[32 * 512];
    static int[] giáTrịTiến = new int[512];
    static int điểmCuốiKếTiếp = 49152;
    static int xácMinh(int sốHiệu) { return sốHiệu >= 32 && sốHiệu < 40 && giáTrịDùng[sốHiệu - 32] != 0 ? sốHiệu - 32 : -1; }
    static boolean cácChồngLấn(int sốHiệu) {
        for (int mụcÔ = 0; mụcÔ < 8; mụcÔ++) if (giáTrịDùng[mụcÔ] != 0 && giáTrịCổng[mụcÔ] == sốHiệu) return true;
        return false;
    }
    static int cổngTạm() {
        for (int giáTrịLầnThử = 0; giáTrịLầnThử < 16; giáTrịLầnThử++) {
            int ứngViên = điểmCuốiKếTiếp++;
            if (điểmCuốiKếTiếp > 65535) điểmCuốiKếTiếp = 49152;
            if (!cácChồngLấn(ứngViên)) return ứngViên;
        }
        return -98;
    }
    public static int tạoMục(int giáTrịMiền, int giáTrịLoại, int giáTrịQuyƯớc) {
        if (giáTrịMiền != 2) return -97;
        if (giáTrịLoại != 2 || (giáTrịQuyƯớc != 0 && giáTrịQuyƯớc != 17)) return -93;
        for (int mụcÔ = 0; mụcÔ < 8; mụcÔ++) if (giáTrịDùng[mụcÔ] == 0) {
            giáTrịDùng[mụcÔ] = 1; giáTrịCổng[mụcÔ] = 0; địaChỉ[mụcÔ] = 0; giáTrịPhíaTrước[mụcÔ] = 0; sốLượngPhầnMục[mụcÔ] = 0; cổngĐãNhận[mụcÔ] = 0;
            return mụcÔ + 32;
        }
        return -24;
    }
    public static int GóiTệpThựcThi(int sốHiệu, int địaChỉMạng, int sốCổngĐiểmCuối) {
        int mụcÔ = xácMinh(sốHiệu);
        if (mụcÔ < 0) return -9;
        if (địaChỉMạng != 0 && địaChỉMạng != 0x7f000001) return -99;
        if (giáTrịCổng[mụcÔ] != 0 || sốCổngĐiểmCuối < 0 || sốCổngĐiểmCuối > 65535) return -22;
        if (sốCổngĐiểmCuối == 0) sốCổngĐiểmCuối = cổngTạm();
        if (sốCổngĐiểmCuối < 0) return sốCổngĐiểmCuối;
        if (cácChồngLấn(sốCổngĐiểmCuối)) return -98;
        giáTrịCổng[mụcÔ] = sốCổngĐiểmCuối; địaChỉ[mụcÔ] = địaChỉMạng; return 0;
    }
    public static int đặtDữLiệu(int sốHiệu, int giáTrị) {
        if (sốHiệu < 0 || sốHiệu >= 512) return -22;
        giáTrịTiến[sốHiệu] = giáTrị & 255; return 0;
    }
    public static int đọcDữLiệu(int sốHiệu) { return sốHiệu >= 0 && sốHiệu < 512 ? giáTrịTiến[sốHiệu] : -22; }
    public static int gửi(int sốHiệu, int địaChỉMạng, int sốCổngĐiểmCuối, int cỡ) {
        int mụcÔ = xácMinh(sốHiệu);
        if (mụcÔ < 0) return -9;
        if (địaChỉMạng != 0x7f000001) return -101;
        if (sốCổngĐiểmCuối < 1 || sốCổngĐiểmCuối > 65535) return -22;
        if (cỡ < 0 || cỡ > 512) return -90;
        if (giáTrịCổng[mụcÔ] == 0) {
            int kếtQuả = GóiTệpThựcThi(sốHiệu, 0x7f000001, 0);
            if (kếtQuả < 0) return kếtQuả;
        }
        int giáTrịĐích = -1;
        for (int ứngViên = 0; ứngViên < 8; ứngViên++) if (giáTrịDùng[ứngViên] != 0 && giáTrịCổng[ứngViên] == sốCổngĐiểmCuối) giáTrịĐích = ứngViên;
        if (giáTrịĐích < 0) return -111;
        if (sốLượngPhầnMục[giáTrịĐích] == 4) return -11;
        int chỉSốVịTrí = giáTrịĐích * 4 + (giáTrịPhíaTrước[giáTrịĐích] + sốLượngPhầnMục[giáTrịĐích]) % 4;
        for (int giáTrịByte = 0; giáTrịByte < cỡ; giáTrịByte++) DữLiệu[chỉSốVịTrí * 512 + giáTrịByte] = giáTrịTiến[giáTrịByte];
        độDài[chỉSốVịTrí] = cỡ; cổngĐãGửi[chỉSốVịTrí] = giáTrịCổng[mụcÔ]; sốLượngPhầnMục[giáTrịĐích]++;
        return cỡ;
    }
    public static int nhận(int sốHiệu, int giáTrịSứcChứa) {
        int mụcÔ = xácMinh(sốHiệu);
        if (mụcÔ < 0) return -9;
        if (giáTrịSứcChứa < 0 || giáTrịSứcChứa > 512) return -22;
        if (sốLượngPhầnMục[mụcÔ] == 0) return -11;
        int chỉSốVịTrí = mụcÔ * 4 + giáTrịPhíaTrước[mụcÔ];
        int cỡ = độDài[chỉSốVịTrí] < giáTrịSứcChứa ? độDài[chỉSốVịTrí] : giáTrịSứcChứa;
        for (int giáTrịByte = 0; giáTrịByte < cỡ; giáTrịByte++) giáTrịTiến[giáTrịByte] = DữLiệu[chỉSốVịTrí * 512 + giáTrịByte];
        cổngĐãNhận[mụcÔ] = cổngĐãGửi[chỉSốVịTrí]; giáTrịPhíaTrước[mụcÔ] = (giáTrịPhíaTrước[mụcÔ] + 1) % 4; sốLượngPhầnMục[mụcÔ]--;
        return cỡ;
    }
    public static int đọcCổngĐiểmCuối(int sốHiệu) { int mụcÔ = xácMinh(sốHiệu); return mụcÔ < 0 ? -9 : giáTrịCổng[mụcÔ]; }
    public static int đọcĐịaChỉ(int sốHiệu) { int mụcÔ = xácMinh(sốHiệu); return mụcÔ < 0 ? -9 : địaChỉ[mụcÔ]; }
    public static int điểmCuốiBộGửi(int sốHiệu) { int mụcÔ = xácMinh(sốHiệu); return mụcÔ < 0 ? -9 : cổngĐãNhận[mụcÔ]; }
    public static int đóng(int sốHiệu) {
        int mụcÔ = xácMinh(sốHiệu); if (mụcÔ < 0) return -9;
        giáTrịDùng[mụcÔ] = 0; sốLượngPhầnMục[mụcÔ] = 0; giáTrịCổng[mụcÔ] = 0; return 0;
    }
}
