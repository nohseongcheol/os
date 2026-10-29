// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Đầu ra chung và xử lý tên tệp ASCII cho công cụ trong máy khách. */
public final class CôngCụJava {
    /** Chuyển mảng byte UTF-8 thành đơn vị UTF-16 ngay trong cùng mảng. Từ chối đầu vào sai dạng. */
    static int giảiMãNguồn(int[] DữLiệu, int độDài) {
        int đọc = 0, ghi = 0;
        if (độDài >= 3 && DữLiệu[0] == 239 && DữLiệu[1] == 187 && DữLiệu[2] == 191) đọc = 3;
        while (đọc < độDài) {
            int giáTrị = DữLiệu[đọc++], trịSố = 0, giáTrịTốiThiểu = 0;
            if (giáTrị >= 194 && giáTrị <= 223) { trịSố = 1; giáTrịTốiThiểu = 128; giáTrị &= 31; }
            else if (giáTrị >= 224 && giáTrị <= 239) { trịSố = 2; giáTrịTốiThiểu = 2048; giáTrị &= 15; }
            else if (giáTrị >= 240 && giáTrị <= 244) { trịSố = 3; giáTrịTốiThiểu = 65536; giáTrị &= 7; }
            else if (giáTrị >= 128 || giáTrị < 0) return -1;
            if (trịSố > độDài - đọc) return -1;
            for (int i = 0; i < trịSố; i++) {
                int phầnMụcKếTiếp = DữLiệu[đọc++]; if ((phầnMụcKếTiếp & 192) != 128) return -1;
                giáTrị = (giáTrị << 6) | (phầnMụcKếTiếp & 63);
            }
            if (giáTrị < giáTrịTốiThiểu || giáTrị > 0x10ffff || (giáTrị >= 0xd800 && giáTrị <= 0xdfff)) return -1;
            if (giáTrị >= 65536) { giáTrị -= 65536; DữLiệu[ghi++] = 0xd800 | (giáTrị >> 10); DữLiệu[ghi++] = 0xdc00 | (giáTrị & 1023); }
            else DữLiệu[ghi++] = giáTrị;
        }
        return ghi;
    }
    static void ghiSố(int giáTrị) {
        if (giáTrị < 0) NgườiDùng.ghiGiáTrịKýTự('-'); else giáTrị = -giáTrị;
        int chỉSốVịTrí = 1000000000;
        boolean chạy = false;
        while (chỉSốVịTrí != 0) {
            int trịSố = -(giáTrị / chỉSốVịTrí);
            if (trịSố != 0 || chạy || chỉSốVịTrí == 1) { NgườiDùng.ghiGiáTrịKýTự('0' + trịSố); chạy = true; }
            giáTrị %= chỉSốVịTrí; chỉSốVịTrí /= 10;
        }
    }
    static int tên(int[] giáTrịĐích, String nguyênBản) {
        if (nguyênBản.length() >= giáTrịĐích.length) return -1;
        for (int trịSố = 0; trịSố < giáTrịĐích.length; trịSố++) giáTrịĐích[trịSố] = trịSố < nguyênBản.length() ? nguyênBản.charAt(trịSố) : 0;
        return nguyênBản.length();
    }
    static boolean vănBảnBằng(String toánHạngĐầuTiên, String toánHạngThứHai) {
        if (toánHạngĐầuTiên.length() != toánHạngThứHai.length()) return false;
        for (int trịSố = 0; trịSố < toánHạngĐầuTiên.length(); trịSố++) if (toánHạngĐầuTiên.charAt(trịSố) != toánHạngThứHai.charAt(trịSố)) return false;
        return true;
    }
}
