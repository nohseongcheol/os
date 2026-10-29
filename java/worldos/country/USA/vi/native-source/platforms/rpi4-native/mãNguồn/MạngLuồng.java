// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Luồng byte có kết nối bên trong nhân: lớp socket vòng về, không phải ngăn xếp gói Ethernet/TCP. */
public final class MạngLuồng {
    static int[] giáTrịTrạngThái = new int[16], giáTrịCổng = new int[16], giáTrịĐãGhépCặp = new int[16], cổngĐốiTác = new int[16], chờGiáTrị = new int[16], làCận = new int[16];
    static int[] giáTrịPhíaTrước = new int[16], trịSố = new int[16], DữLiệu = new int[16 * 1024];
    static int phầnMụcKếTiếp = 50000;
    static int xácMinh(int sốTệpĐãMở) { return sốTệpĐãMở >= 40 && sốTệpĐãMở < 56 && giáTrịTrạngThái[sốTệpĐãMở - 40] != 0 ? sốTệpĐãMở - 40 : -1; }
    static boolean làDùngTrong(int sốCổng) { for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < 16; chỉSốVòngLặp++) if (giáTrịTrạngThái[chỉSốVòngLặp] != 0 && làCận[chỉSốVòngLặp] != 0 && giáTrịCổng[chỉSốVòngLặp] == sốCổng) return true; return false; }
    public static int tạoMục() {
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < 16; chỉSốVòngLặp++) if (giáTrịTrạngThái[chỉSốVòngLặp] == 0) { giáTrịTrạngThái[chỉSốVòngLặp] = 1; cổngĐốiTác[chỉSốVòngLặp] = giáTrịCổng[chỉSốVòngLặp] = giáTrịPhíaTrước[chỉSốVòngLặp] = trịSố[chỉSốVòngLặp] = chờGiáTrị[chỉSốVòngLặp] = làCận[chỉSốVòngLặp] = 0; giáTrịĐãGhépCặp[chỉSốVòngLặp] = -1; return chỉSốVòngLặp + 40; }
        return -24;
    }
    public static int GóiTệpThựcThi(int sốTệpĐãMở, int ĐịaChỉỔCắmMạng, int sốCổng) {
        int chỉSốVòngLặp = xácMinh(sốTệpĐãMở); if (chỉSốVòngLặp < 0) return -9;
        if (ĐịaChỉỔCắmMạng != 0 && ĐịaChỉỔCắmMạng != 0x7f000001) return -99;
        if (giáTrịTrạngThái[chỉSốVòngLặp] != 1 || sốCổng < 0 || sốCổng > 65535) return -22;
        if (sốCổng == 0) { do { sốCổng = phầnMụcKếTiếp++; if (phầnMụcKếTiếp > 65535) phầnMụcKếTiếp = 50000; } while (làDùngTrong(sốCổng)); }
        if (làDùngTrong(sốCổng)) return -98; giáTrịCổng[chỉSốVòngLặp] = sốCổng; làCận[chỉSốVòngLặp] = 1; giáTrịTrạngThái[chỉSốVòngLặp] = 2; return 0;
    }
    public static int lắngNgheĐiểmCuối(int sốTệpĐãMở, int hàngĐợiChờ) { int chỉSốVòngLặp = xácMinh(sốTệpĐãMở); if (chỉSốVòngLặp < 0) return -9; if (giáTrịTrạngThái[chỉSốVòngLặp] != 2 || hàngĐợiChờ < 1) return -22; giáTrịTrạngThái[chỉSốVòngLặp] = 3; return 0; }
    public static int nốiKết(int sốTệpĐãMở, int ĐịaChỉỔCắmMạng, int sốCổng) {
        int chỉSốVòngLặp = xácMinh(sốTệpĐãMở); if (chỉSốVòngLặp < 0) return -9; if (ĐịaChỉỔCắmMạng != 0x7f000001) return -101;
        if (sốCổng < 1 || sốCổng > 65535 || giáTrịTrạngThái[chỉSốVòngLặp] > 2) return -22;
        int nhậnTrang = -1; for (int vịTríPhíaTrong = 0; vịTríPhíaTrong < 16; vịTríPhíaTrong++) if (giáTrịTrạngThái[vịTríPhíaTrong] == 3 && giáTrịCổng[vịTríPhíaTrong] == sốCổng) nhậnTrang = vịTríPhíaTrong;
        if (nhậnTrang < 0) return -111;
        int làĐãXếpHàng = 0; for (int vịTríPhíaTrong = 0; vịTríPhíaTrong < 16; vịTríPhíaTrong++) if (chờGiáTrị[vịTríPhíaTrong] == nhậnTrang + 1) làĐãXếpHàng++;
        if (làĐãXếpHàng >= 4) return -11;
        if (giáTrịTrạngThái[chỉSốVòngLặp] == 1) { int giáTrịĐãXửLý = GóiTệpThựcThi(sốTệpĐãMở, 0x7f000001, 0); if (giáTrịĐãXửLý < 0) return giáTrịĐãXửLý; }
        int khác = tạoMục(); if (khác < 0) return khác; khác -= 40;
        giáTrịTrạngThái[chỉSốVòngLặp] = giáTrịTrạngThái[khác] = 4; giáTrịĐãGhépCặp[chỉSốVòngLặp] = khác; giáTrịĐãGhépCặp[khác] = chỉSốVòngLặp; giáTrịCổng[khác] = sốCổng; cổngĐốiTác[chỉSốVòngLặp] = sốCổng; cổngĐốiTác[khác] = giáTrịCổng[chỉSốVòngLặp]; chờGiáTrị[khác] = nhậnTrang + 1; return 0;
    }
    public static int chấpNhậnKếtNối(int sốTệpĐãMở) { int chỉSốVòngLặp = xácMinh(sốTệpĐãMở); if (chỉSốVòngLặp < 0) return -9; if (giáTrịTrạngThái[chỉSốVòngLặp] != 3) return -22; for (int vịTríPhíaTrong = 0; vịTríPhíaTrong < 16; vịTríPhíaTrong++) if (giáTrịTrạngThái[vịTríPhíaTrong] != 0 && chờGiáTrị[vịTríPhíaTrong] == chỉSốVòngLặp + 1) { chờGiáTrị[vịTríPhíaTrong] = 0; return vịTríPhíaTrong + 40; } return -11; }
    public static int ghi(int sốTệpĐãMở, int sốLượngMục) {
        int chỉSốVòngLặp = xácMinh(sốTệpĐãMở); if (chỉSốVòngLặp < 0) return -9; if (giáTrịTrạngThái[chỉSốVòngLặp] != 4) return -107;
        if (sốLượngMục < 0 || sốLượngMục > 512) return -22; if (sốLượngMục == 0) return 0;
        int vịTríPhíaTrong = giáTrịĐãGhépCặp[chỉSốVòngLặp]; if (vịTríPhíaTrong < 0) return -32; int sốLượngTổngCộng = 1024 - trịSố[vịTríPhíaTrong]; if (sốLượngTổngCộng == 0) return -11; if (sốLượngTổngCộng > sốLượngMục) sốLượngTổngCộng = sốLượngMục;
        for (int vịTríPhépSoSánh = 0; vịTríPhépSoSánh < sốLượngTổngCộng; vịTríPhépSoSánh++) DữLiệu[vịTríPhíaTrong * 1024 + (giáTrịPhíaTrước[vịTríPhíaTrong] + trịSố[vịTríPhíaTrong] + vịTríPhépSoSánh) % 1024] = MạngVòngVề.giáTrịTiến[vịTríPhépSoSánh]; trịSố[vịTríPhíaTrong] += sốLượngTổngCộng; return sốLượngTổngCộng;
    }
    public static int đọc(int sốTệpĐãMở, int sốLượngMục) {
        int chỉSốVòngLặp = xácMinh(sốTệpĐãMở); if (chỉSốVòngLặp < 0) return -9; if (giáTrịTrạngThái[chỉSốVòngLặp] != 4) return -107; if (sốLượngMục < 0 || sốLượngMục > 512) return -22;
        if (sốLượngMục == 0) return 0; if (trịSố[chỉSốVòngLặp] == 0) return giáTrịĐãGhépCặp[chỉSốVòngLặp] < 0 ? 0 : -11; if (sốLượngMục > trịSố[chỉSốVòngLặp]) sốLượngMục = trịSố[chỉSốVòngLặp];
        for (int vịTríPhépSoSánh = 0; vịTríPhépSoSánh < sốLượngMục; vịTríPhépSoSánh++) MạngVòngVề.giáTrịTiến[vịTríPhépSoSánh] = DữLiệu[chỉSốVòngLặp * 1024 + (giáTrịPhíaTrước[chỉSốVòngLặp] + vịTríPhépSoSánh) % 1024]; giáTrịPhíaTrước[chỉSốVòngLặp] = (giáTrịPhíaTrước[chỉSốVòngLặp] + sốLượngMục) % 1024; trịSố[chỉSốVòngLặp] -= sốLượngMục; return sốLượngMục;
    }
    public static int đọcCổngĐiểmCuối(int sốTệpĐãMở) { int chỉSốVòngLặp = xácMinh(sốTệpĐãMở); return chỉSốVòngLặp < 0 ? -9 : giáTrịCổng[chỉSốVòngLặp]; }
    public static int đọcCổngĐốiTác(int sốTệpĐãMở) { int chỉSốVòngLặp = xácMinh(sốTệpĐãMở); return chỉSốVòngLặp < 0 ? -9 : cổngĐốiTác[chỉSốVòngLặp]; }
    public static int đóng(int sốTệpĐãMở) {
        int chỉSốVòngLặp = xácMinh(sốTệpĐãMở); if (chỉSốVòngLặp < 0) return -9;
        if (giáTrịTrạngThái[chỉSốVòngLặp] == 3) for (int vịTríPhíaTrong = 0; vịTríPhíaTrong < 16; vịTríPhíaTrong++) if (chờGiáTrị[vịTríPhíaTrong] == chỉSốVòngLặp + 1) { if (giáTrịĐãGhépCặp[vịTríPhíaTrong] >= 0) giáTrịĐãGhépCặp[giáTrịĐãGhépCặp[vịTríPhíaTrong]] = -1; giáTrịTrạngThái[vịTríPhíaTrong] = chờGiáTrị[vịTríPhíaTrong] = làCận[vịTríPhíaTrong] = 0; }
        if (giáTrịĐãGhépCặp[chỉSốVòngLặp] >= 0) giáTrịĐãGhépCặp[giáTrịĐãGhépCặp[chỉSốVòngLặp]] = -1; giáTrịTrạngThái[chỉSốVòngLặp] = làCận[chỉSốVòngLặp] = trịSố[chỉSốVòngLặp] = chờGiáTrị[chỉSốVòngLặp] = 0; return 0;
    }
}
