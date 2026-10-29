// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class VàoRaThiếtBịCuối {
    static void KýTự(int giáTrị) {
        if (giáTrị < 0x80) BoMạch.ghiNốiTiếp(giáTrị);
        else if (giáTrị < 0x800) {
            BoMạch.ghiNốiTiếp(0xc0 | (giáTrị >> 6)); BoMạch.ghiNốiTiếp(0x80 | (giáTrị & 63));
        } else if (giáTrị < 0x10000) {
            BoMạch.ghiNốiTiếp(0xe0 | (giáTrị >> 12)); BoMạch.ghiNốiTiếp(0x80 | ((giáTrị >> 6) & 63)); BoMạch.ghiNốiTiếp(0x80 | (giáTrị & 63));
        } else {
            BoMạch.ghiNốiTiếp(0xf0 | (giáTrị >> 18)); BoMạch.ghiNốiTiếp(0x80 | ((giáTrị >> 12) & 63));
            BoMạch.ghiNốiTiếp(0x80 | ((giáTrị >> 6) & 63)); BoMạch.ghiNốiTiếp(0x80 | (giáTrị & 63));
        }
    }
    static void ghi(String vănBản) {
        for (int sốHiệu = 0; sốHiệu < vănBản.length(); sốHiệu++) {
            int giáTrị = vănBản.charAt(sốHiệu);
            if (giáTrị >= 0xd800 && giáTrị <= 0xdbff && sốHiệu + 1 < vănBản.length()) {
                int giáTrịĐáy = vănBản.charAt(sốHiệu + 1);
                if (giáTrịĐáy >= 0xdc00 && giáTrịĐáy <= 0xdfff) {
                    giáTrị = 0x10000 + ((giáTrị - 0xd800) << 10) + giáTrịĐáy - 0xdc00; sốHiệu++;
                }
            }
            if (giáTrị >= 0xd800 && giáTrị <= 0xdfff) giáTrị = 0xfffd;
            KýTự(giáTrị);
        }
    }
    static void trịSố(int giáTrị) {
        if (giáTrị < 0) KýTự('-'); else giáTrị = -giáTrị;
        int chỉSốVịTrí = 1000000000;
        boolean chạy = false;
        while (chỉSốVịTrí > 0) {
            int giáTrịChữSố = -(giáTrị / chỉSốVịTrí);
            if (giáTrịChữSố != 0 || chạy || chỉSốVịTrí == 1) { KýTự('0' + giáTrịChữSố); chạy = true; }
            giáTrị %= chỉSốVịTrí; chỉSốVịTrí /= 10;
        }
    }
}
