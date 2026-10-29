// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Định dạng lưu trữ riêng nhỏ dùng tổng kiểm và hai bản sao. Chỉ ghi bền vững khi fsync/sync. */
public final class LưuGiữTệp {
    static int saoChépĐãGiữNguyênHiệnTại = -1, sốThếHệ = 0;
    static int[] bảngTraTệp = new int[1024];
    static int cácByteMãBăm(int giáTrị, int DữLiệu) { return (giáTrị ^ DữLiệu) * 16777619; }
    static void xóaSạchDữLiệu() {
        for (int sốHiệu = 0; sốHiệu < 512; sốHiệu++) KếtNốiLưuTrữ.dữLiệuMụcĐoạn[sốHiệu] = 0;
    }
    static int sốNguyênBảngTra(int vịTrí) {
        return bảngTraTệp[vịTrí] | bảngTraTệp[vịTrí + 1] << 8 | bảngTraTệp[vịTrí + 2] << 16 | bảngTraTệp[vịTrí + 3] << 24;
    }
    static void ghiSốNguyênBảngTra(int vịTrí, int giáTrị) {
        for (int sốHiệu = 0; sốHiệu < 4; sốHiệu++) bảngTraTệp[vịTrí + sốHiệu] = (giáTrị >>> (sốHiệu * 8)) & 255;
    }
    static boolean kiểmTraBảngTra() {
        for (int Tệp = 0; Tệp < 8; Tệp++) {
            int độDài = 0;
            for (int mụcÔ = 0; mụcÔ < 64; mụcÔ++) HệTệpBộNhớ.tên[mụcÔ] = bảngTraTệp[Tệp * 72 + mụcÔ];
            while (độDài < 64 && HệTệpBộNhớ.tên[độDài] != 0) độDài++;
            if (độDài == 0) continue;
            if (!HệTệpBộNhớ.kiểmTraTên(HệTệpBộNhớ.tên, độDài)
                || sốNguyênBảngTra(Tệp * 72 + 64) < 0 || sốNguyênBảngTra(Tệp * 72 + 64) > 16384) return false;
            for (int giáTrịPhíaTrước = 0; giáTrịPhíaTrước < Tệp; giáTrịPhíaTrước++) {
                boolean vănBảnBằng = bảngTraTệp[giáTrịPhíaTrước * 72 + độDài] == 0;
                for (int mụcÔ = 0; mụcÔ < độDài; mụcÔ++) if (bảngTraTệp[giáTrịPhíaTrước * 72 + mụcÔ] != HệTệpBộNhớ.tên[mụcÔ]) vănBảnBằng = false;
                if (vănBảnBằng) return false;
            }
        }
        return true;
    }
    static int kiểmTraSaoChépĐãGiữNguyên(int saoChépĐãGiữNguyên) {
        int bắtChạyMụcĐoạn = 1 + saoChépĐãGiữNguyên * 259;
        if (KếtNốiLưuTrữ.đọc(bắtChạyMụcĐoạn) < 0 || KếtNốiLưuTrữ.phânTíchCúPhápSốNguyên(0) != 0x4a4b534e) return -1;
        int giáTrịThếHệ = KếtNốiLưuTrữ.phânTíchCúPhápSốNguyên(4), tổngKiểm = KếtNốiLưuTrữ.phânTíchCúPhápSốNguyên(8);
        if (giáTrịThếHệ < 1 || KếtNốiLưuTrữ.phânTíchCúPhápSốNguyên(12) != (giáTrịThếHệ ^ tổngKiểm ^ 0x4a4b534e)) return -1;
        int tệpMãBăm = 0x811c9dc5;
        for (int giáTrịMụcĐoạn = 0; giáTrịMụcĐoạn < 258; giáTrịMụcĐoạn++) {
            if (KếtNốiLưuTrữ.đọc(bắtChạyMụcĐoạn + 1 + giáTrịMụcĐoạn) < 0) return -1;
            for (int mụcÔ = 0; mụcÔ < 512; mụcÔ++) {
                int giáTrị = KếtNốiLưuTrữ.dữLiệuMụcĐoạn[mụcÔ];
                tệpMãBăm = cácByteMãBăm(tệpMãBăm, giáTrị);
                if (giáTrịMụcĐoạn < 2) bảngTraTệp[giáTrịMụcĐoạn * 512 + mụcÔ] = giáTrị;
            }
        }
        return tệpMãBăm == tổngKiểm && kiểmTraBảngTra() ? giáTrịThếHệ : -1;
    }
    static int nạp(int saoChépĐãGiữNguyên) {
        int bắtChạyMụcĐoạn = 1 + saoChépĐãGiữNguyên * 259;
        for (int giáTrịMụcĐoạn = 0; giáTrịMụcĐoạn < 2; giáTrịMụcĐoạn++) {
            if (KếtNốiLưuTrữ.đọc(bắtChạyMụcĐoạn + 1 + giáTrịMụcĐoạn) < 0) return -5;
            for (int mụcÔ = 0; mụcÔ < 512; mụcÔ++) bảngTraTệp[giáTrịMụcĐoạn * 512 + mụcÔ] = KếtNốiLưuTrữ.dữLiệuMụcĐoạn[mụcÔ];
        }
        for (int Tệp = 0; Tệp < 8; Tệp++) {
            for (int mụcÔ = 0; mụcÔ < 64; mụcÔ++) HệTệpBộNhớ.danhSáchCácTên[Tệp * 64 + mụcÔ] = bảngTraTệp[Tệp * 72 + mụcÔ];
            HệTệpBộNhớ.danhSáchCỡ[Tệp] = bảngTraTệp[Tệp * 72] == 0 ? 0 : sốNguyênBảngTra(Tệp * 72 + 64);
            HệTệpBộNhớ.cácQuyềnĐượcCấpQuyền[Tệp] = sốNguyênBảngTra(Tệp * 72 + 68) & 511;
            for (int giáTrịMụcĐoạn = 0; giáTrịMụcĐoạn < 32; giáTrịMụcĐoạn++) {
                if (KếtNốiLưuTrữ.đọc(bắtChạyMụcĐoạn + 3 + Tệp * 32 + giáTrịMụcĐoạn) < 0) return -5;
                int địaChỉ = ThiếtBị.bộNhớTệp() + Tệp * 16384 + giáTrịMụcĐoạn * 512;
                for (int mụcÔ = 0; mụcÔ < 512; mụcÔ++) ThiếtBị.ghiBộNhớ(địaChỉ + mụcÔ, KếtNốiLưuTrữ.dữLiệuMụcĐoạn[mụcÔ]);
            }
        }
        return 0;
    }
    static void chuẩnBị() {
        if (KếtNốiLưuTrữ.đọc(0) < 0 || KếtNốiLưuTrữ.phânTíchCúPhápSốNguyên(0) != 0x54534b4a
            || KếtNốiLưuTrữ.phânTíchCúPhápSốNguyên(4) != 0x3145524f || KếtNốiLưuTrữ.phânTíchCúPhápSốNguyên(8) != 2048
            || KếtNốiLưuTrữ.phânTíchCúPhápSốNguyên(12) != 0x3153464a) {
            ĐầuCuốiVănBản.ghi("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        KếtNốiLưuTrữ.làSẵnCó = true;
        int thứBậcĐầuTiên = kiểmTraSaoChépĐãGiữNguyên(0), thứBậcThứHai = kiểmTraSaoChépĐãGiữNguyên(1);
        if (thứBậcĐầuTiên < 0 && thứBậcThứHai < 0) { ĐầuCuốiVănBản.ghi("STORE ready; no valid snapshot\n"); return; }
        saoChépĐãGiữNguyênHiệnTại = thứBậcĐầuTiên >= thứBậcThứHai ? 0 : 1; sốThếHệ = thứBậcĐầuTiên >= thứBậcThứHai ? thứBậcĐầuTiên : thứBậcThứHai;
        if (nạp(saoChépĐãGiữNguyênHiệnTại) < 0) {
            ĐầuCuốiVănBản.ghi("STORE read failed; halted to preserve files\n"); ThiếtBị.việcThựcThiDừngHẳn();
        }
        ĐầuCuốiVănBản.ghi("STORE restored generation "); ĐầuCuốiVănBản.ghiSố(sốThếHệ); ĐầuCuốiVănBản.KýTự(10);
    }
    static int đồngBộHóa() {
        if (!KếtNốiLưuTrữ.làSẵnCó) return -19;
        if (sốThếHệ == 2147483647) return -75;
        int phầnMụcKếTiếp = saoChépĐãGiữNguyênHiệnTại == 0 ? 1 : 0, bắtChạyMụcĐoạn = 1 + phầnMụcKếTiếp * 259;
        // Vô hiệu hóa commit cũ và đẩy bộ nhớ đệm thiết bị trước khi ghi thân mới.
        xóaSạchDữLiệu();
        if (KếtNốiLưuTrữ.ghi(bắtChạyMụcĐoạn) < 0 || KếtNốiLưuTrữ.đầuRaĐẩyĐệm() < 0) return -5;
        for (int mụcÔ = 0; mụcÔ < 1024; mụcÔ++) bảngTraTệp[mụcÔ] = 0;
        for (int Tệp = 0; Tệp < 8; Tệp++) if (HệTệpBộNhớ.danhSáchCácTên[Tệp * 64] != 0) {
            for (int mụcÔ = 0; mụcÔ < 64; mụcÔ++) bảngTraTệp[Tệp * 72 + mụcÔ] = HệTệpBộNhớ.danhSáchCácTên[Tệp * 64 + mụcÔ];
            ghiSốNguyênBảngTra(Tệp * 72 + 64, HệTệpBộNhớ.danhSáchCỡ[Tệp]);
            ghiSốNguyênBảngTra(Tệp * 72 + 68, HệTệpBộNhớ.cácQuyềnĐượcCấpQuyền[Tệp]);
        }
        int tệpMãBăm = 0x811c9dc5;
        for (int giáTrịMụcĐoạn = 0; giáTrịMụcĐoạn < 258; giáTrịMụcĐoạn++) {
            for (int mụcÔ = 0; mụcÔ < 512; mụcÔ++) {
                int giáTrị = 0;
                if (giáTrịMụcĐoạn < 2) giáTrị = bảngTraTệp[giáTrịMụcĐoạn * 512 + mụcÔ];
                else {
                    int Tệp = (giáTrịMụcĐoạn - 2) / 32, vịTrí = (giáTrịMụcĐoạn - 2) % 32 * 512 + mụcÔ;
                    if (bảngTraTệp[Tệp * 72] != 0 && vịTrí < HệTệpBộNhớ.danhSáchCỡ[Tệp])
                        giáTrị = ThiếtBị.đọcBộNhớ(ThiếtBị.bộNhớTệp() + Tệp * 16384 + vịTrí);
                }
                KếtNốiLưuTrữ.dữLiệuMụcĐoạn[mụcÔ] = giáTrị; tệpMãBăm = cácByteMãBăm(tệpMãBăm, giáTrị);
            }
            if (KếtNốiLưuTrữ.ghi(bắtChạyMụcĐoạn + 1 + giáTrịMụcĐoạn) < 0) return -5;
        }
        if (KếtNốiLưuTrữ.đầuRaĐẩyĐệm() < 0) return -5;
        xóaSạchDữLiệu(); KếtNốiLưuTrữ.ghiGiáTrịSốNguyên(0, 0x4a4b534e);
        KếtNốiLưuTrữ.ghiGiáTrịSốNguyên(4, sốThếHệ + 1); KếtNốiLưuTrữ.ghiGiáTrịSốNguyên(8, tệpMãBăm);
        KếtNốiLưuTrữ.ghiGiáTrịSốNguyên(12, (sốThếHệ + 1) ^ tệpMãBăm ^ 0x4a4b534e);
        if (KếtNốiLưuTrữ.ghi(bắtChạyMụcĐoạn) < 0 || KếtNốiLưuTrữ.đầuRaĐẩyĐệm() < 0) return -5;
        saoChépĐãGiữNguyênHiệnTại = phầnMụcKếTiếp; sốThếHệ++;
        return 0;
    }
}
