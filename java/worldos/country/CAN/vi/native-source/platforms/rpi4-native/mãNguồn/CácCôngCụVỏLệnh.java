// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Công cụ tích hợp của trình thông dịch lệnh dùng chung RAM VFS và vào ra tiêu chuẩn. */
public final class CácCôngCụVỏLệnh {
    static int[] DữLiệu = new int[16384];
    static int tệpĐầuVào = -1;
    static int mởTệp(int chỉSốĐốiSố, int chếĐộTiếnTrình) {
        int giáTrịĐãXửLý = TrìnhThôngDịchLệnh.đườngDẫn(chỉSốĐốiSố); return giáTrịĐãXửLý < 0 ? giáTrịĐãXửLý : CácTệpBộNhớ.mở(chếĐộTiếnTrình);
    }
    static boolean chuẩnBịĐầuVào(int chỉSốĐốiSố) {
        tệpĐầuVào = -1;
        if (chỉSốĐốiSố < TrìnhThôngDịchLệnh.sốLượngTừTố) {
            tệpĐầuVào = mởTệp(chỉSốĐốiSố, 0);
            if (tệpĐầuVào < 0) { TrìnhThôngDịchLệnh.lỗi(tệpĐầuVào); return false; }
        }
        return true;
    }
    static int đọc() {
        if (tệpĐầuVào >= 3) return CácTệpBộNhớ.đọc(tệpĐầuVào);
        while (true) {
            int dữLiệuByte = BoMạch.đọcNốiTiếp(); if (dữLiệuByte == -2 || dữLiệuByte == 4) return 256;
            if (dữLiệuByte == 3) { TrìnhThôngDịchLệnh.kếtQuả = 130; return 256; }
            if (dữLiệuByte >= 0) return dữLiệuByte; BoMạch.nhườngBộXửLýTrungTâm();
        }
    }
    static void đóng() { if (tệpĐầuVào >= 3) CácTệpBộNhớ.đóng(tệpĐầuVào); tệpĐầuVào = -1; }
    static void giáTrịKhungNhìn() {
        int vịTríCuối = TrìnhThôngDịchLệnh.sốLượngTừTố == 1 ? 2 : TrìnhThôngDịchLệnh.sốLượngTừTố;
        for (int chỉSốĐốiSố = 1; chỉSốĐốiSố < vịTríCuối; chỉSốĐốiSố++) {
            if (!chuẩnBịĐầuVào(chỉSốĐốiSố)) continue;
            int dữLiệuByte; while ((dữLiệuByte = đọc()) != 256 && dữLiệuByte >= 0) BoMạch.ghiNốiTiếp(dữLiệuByte);
            if (dữLiệuByte < 0) TrìnhThôngDịchLệnh.lỗi(dữLiệuByte); đóng();
        }
    }
    static void côngViệcTệp(String sốHànhĐộng) {
        if (TrìnhThôngDịchLệnh.sốLượngTừTố != 2) { TrìnhThôngDịchLệnh.kếtQuả = 2; VàoRaThiếtBịCuối.ghi("사용법: mkdir/rmdir/touch Tệp\n"); return; }
        int giáTrịĐãXửLý = TrìnhThôngDịchLệnh.đườngDẫn(1);
        if (giáTrịĐãXửLý >= 0) {
            if (sốHànhĐộng.charAt(0) == 'm') giáTrịĐãXửLý = CácTệpBộNhớ.tạoThưMục();
            else if (sốHànhĐộng.charAt(0) == 'r') giáTrịĐãXửLý = CácTệpBộNhớ.gỡThưMục();
            else { giáTrịĐãXửLý = CácTệpBộNhớ.mở(65); if (giáTrịĐãXửLý >= 3) giáTrịĐãXửLý = CácTệpBộNhớ.đóng(giáTrịĐãXửLý); }
        }
        if (giáTrịĐãXửLý < 0) TrìnhThôngDịchLệnh.lỗi(giáTrịĐãXửLý);
    }
    static void saoChépGiáTrị(boolean cóĐãDiChuyển) {
        if (TrìnhThôngDịchLệnh.sốLượngTừTố != 3) { TrìnhThôngDịchLệnh.kếtQuả = 2; VàoRaThiếtBịCuối.ghi("사용법: cp/mv nguyênBản điểmCuốiĐích (Tệp)\n"); return; }
        int giáTrịĐãXửLý = TrìnhThôngDịchLệnh.đườngDẫn(1); if (giáTrịĐãXửLý >= 0) giáTrịĐãXửLý = CácTệpBộNhớ.chuẩnHóaGiáTrị();
        if (giáTrịĐãXửLý < 0) { TrìnhThôngDịchLệnh.lỗi(giáTrịĐãXửLý); return; }
        int sốNguyênBản = CácTệpBộNhớ.tìmMục(); if (sốNguyênBản < 0) { TrìnhThôngDịchLệnh.lỗi(-2); return; }
        int sốLượngMục = CácTệpBộNhớ.độDài[sốNguyênBản]; for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < sốLượngMục; chỉSốVòngLặp++) DữLiệu[chỉSốVòngLặp] = CácTệpBộNhớ.đọcDữLiệu(sốNguyênBản, chỉSốVòngLặp);
        giáTrịĐãXửLý = TrìnhThôngDịchLệnh.đườngDẫn(2); if (giáTrịĐãXửLý >= 0) giáTrịĐãXửLý = CácTệpBộNhớ.chuẩnHóaGiáTrị();
        if (giáTrịĐãXửLý < 0) { TrìnhThôngDịchLệnh.lỗi(giáTrịĐãXửLý); return; }
        if (CácTệpBộNhớ.tìmMục() == sốNguyênBản) { if (!cóĐãDiChuyển) TrìnhThôngDịchLệnh.lỗi(-22); return; }
        if (cóĐãDiChuyển) { giáTrịĐãXửLý = CácTệpBộNhớ.đổiTênMục(sốNguyênBản); if (giáTrịĐãXửLý < 0) TrìnhThôngDịchLệnh.lỗi(giáTrịĐãXửLý); return; }
        int sốTệpĐãMở = CácTệpBộNhớ.mở(577); if (sốTệpĐãMở < 0) { TrìnhThôngDịchLệnh.lỗi(sốTệpĐãMở); return; }
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < sốLượngMục; chỉSốVòngLặp++) { giáTrịĐãXửLý = CácTệpBộNhớ.ghi(sốTệpĐãMở, DữLiệu[chỉSốVòngLặp]); if (giáTrịĐãXửLý < 0) { TrìnhThôngDịchLệnh.lỗi(giáTrịĐãXửLý); break; } }
        CácTệpBộNhớ.đóng(sốTệpĐãMở);
    }
    static int giáTrịChữSố(int chỉSốĐốiSố) {
        if (chỉSốĐốiSố >= TrìnhThôngDịchLệnh.sốLượngTừTố) return -1;
        int sốLượngMục = 0; for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < TrìnhThôngDịchLệnh.độDài[chỉSốĐốiSố]; chỉSốVòngLặp++) { int mãKýTự = TrìnhThôngDịchLệnh.giáTrịTừTố[TrìnhThôngDịchLệnh.điểmĐangBắtChạy[chỉSốĐốiSố] + chỉSốVòngLặp]; if (mãKýTự < '0' || mãKýTự > '9' || sốLượngMục > 10000) return -1; sốLượngMục = sốLượngMục * 10 + mãKýTự - '0'; } return sốLượngMục;
    }
    static void giáTrịViệcĐếm() {
        int chỉSốĐốiSố = 1, tùyChọn = 0;
        if (TrìnhThôngDịchLệnh.vănBảnBằng(1, "-c") || TrìnhThôngDịchLệnh.vănBảnBằng(1, "-l") || TrìnhThôngDịchLệnh.vănBảnBằng(1, "-w")) { tùyChọn = TrìnhThôngDịchLệnh.vănBảnBằng(1, "-c") ? 1 : TrìnhThôngDịchLệnh.vănBảnBằng(1, "-l") ? 2 : 3; chỉSốĐốiSố++; }
        if (TrìnhThôngDịchLệnh.sốLượngTừTố > chỉSốĐốiSố + 1) { TrìnhThôngDịchLệnh.kếtQuả = 2; VàoRaThiếtBịCuối.ghi("사용법: wc [-c|-l|-w] [Tệp]\n"); return; }
        if (!chuẩnBịĐầuVào(chỉSốĐốiSố)) return;
        int sốLượngByte = 0, cácDòng = 0, sốLượngTừTừVựng = 0, dữLiệuByte; boolean từTừVựng = false;
        while ((dữLiệuByte = đọc()) >= 0 && dữLiệuByte != 256) { sốLượngByte++; if (dữLiệuByte == 10) cácDòng++; boolean khôngGian = dữLiệuByte == 32 || dữLiệuByte >= 9 && dữLiệuByte <= 13; if (!khôngGian && !từTừVựng) sốLượngTừTừVựng++; từTừVựng = !khôngGian; }
        đóng(); if (dữLiệuByte < 0) { TrìnhThôngDịchLệnh.lỗi(dữLiệuByte); return; }
        if (tùyChọn != 0) VàoRaThiếtBịCuối.trịSố(tùyChọn == 1 ? sốLượngByte : tùyChọn == 2 ? cácDòng : sốLượngTừTừVựng);
        else { VàoRaThiếtBịCuối.trịSố(cácDòng); VàoRaThiếtBịCuối.KýTự(' '); VàoRaThiếtBịCuối.trịSố(sốLượngTừTừVựng); VàoRaThiếtBịCuối.KýTự(' '); VàoRaThiếtBịCuối.trịSố(sốLượngByte); } VàoRaThiếtBịCuối.KýTự(10);
    }
    static void tìmMục() {
        if (TrìnhThôngDịchLệnh.sốLượngTừTố < 2 || TrìnhThôngDịchLệnh.sốLượngTừTố > 3) { TrìnhThôngDịchLệnh.kếtQuả = 2; VàoRaThiếtBịCuối.ghi("사용법: grep 찾을문구 [Tệp]\n"); return; }
        if (!chuẩnBịĐầuVào(2)) return;
        int sốLượngMục = 0, dữLiệuByte, cácKếtQuảKhớp = 0;
        while (true) {
            dữLiệuByte = đọc();
            if (dữLiệuByte == 10 || dữLiệuByte == 256 || dữLiệuByte < 0) {
                boolean đãTìmThấyĐãLà = false;
                for (int chỉSốVòngLặp = 0; chỉSốVòngLặp <= sốLượngMục - TrìnhThôngDịchLệnh.độDài[1]; chỉSốVòngLặp++) {
                    boolean làGiốngNhau = true; for (int vịTríPhíaTrong = 0; vịTríPhíaTrong < TrìnhThôngDịchLệnh.độDài[1]; vịTríPhíaTrong++) if (DữLiệu[chỉSốVòngLặp + vịTríPhíaTrong] != TrìnhThôngDịchLệnh.giáTrịTừTố[TrìnhThôngDịchLệnh.điểmĐangBắtChạy[1] + vịTríPhíaTrong]) làGiốngNhau = false;
                    if (làGiốngNhau) đãTìmThấyĐãLà = true;
                }
                if (đãTìmThấyĐãLà && (sốLượngMục > 0 || dữLiệuByte == 10)) { for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < sốLượngMục; chỉSốVòngLặp++) BoMạch.ghiNốiTiếp(DữLiệu[chỉSốVòngLặp]); VàoRaThiếtBịCuối.KýTự(10); cácKếtQuảKhớp++; }
                sốLượngMục = 0; if (dữLiệuByte != 10) break;
            } else if (sốLượngMục < DữLiệu.length) DữLiệu[sốLượngMục++] = dữLiệuByte;
            else { TrìnhThôngDịchLệnh.lỗi(-28); đóng(); return; }
        }
        đóng(); if (dữLiệuByte < 0) TrìnhThôngDịchLệnh.lỗi(dữLiệuByte); else if (TrìnhThôngDịchLệnh.kếtQuả == 0) TrìnhThôngDịchLệnh.kếtQuả = cácKếtQuảKhớp == 0 ? 1 : 0;
    }
    static void giáTrịĐầu(boolean vịTríPhíaSau) {
        int chỉSốĐốiSố = 1, cácDòng = 10;
        if (TrìnhThôngDịchLệnh.vănBảnBằng(1, "-n")) { cácDòng = giáTrịChữSố(2); chỉSốĐốiSố = 3; }
        if (cácDòng < 0 || TrìnhThôngDịchLệnh.sốLượngTừTố > chỉSốĐốiSố + 1) { TrìnhThôngDịchLệnh.kếtQuả = 2; VàoRaThiếtBịCuối.ghi("사용법: head/tail [-n cácDòng] [Tệp]\n"); return; }
        if (!chuẩnBịĐầuVào(chỉSốĐốiSố)) return;
        int sốLượngMục = 0, dữLiệuByte;
        while ((dữLiệuByte = đọc()) != 256 && dữLiệuByte >= 0) { if (sốLượngMục == DữLiệu.length) { TrìnhThôngDịchLệnh.lỗi(-28); đóng(); return; } DữLiệu[sốLượngMục++] = dữLiệuByte; }
        đóng(); if (dữLiệuByte < 0) { TrìnhThôngDịchLệnh.lỗi(dữLiệuByte); return; }
        int bắtChạyCụcBộ = 0, vịTríKếtThúc = sốLượngMục;
        if (cácDòng == 0) return;
        if (vịTríPhíaSau) { int sốLượngTổngCộng = 0; for (int chỉSốVòngLặp = sốLượngMục - 2; chỉSốVòngLặp >= 0; chỉSốVòngLặp--) if (DữLiệu[chỉSốVòngLặp] == 10 && ++sốLượngTổngCộng == cácDòng) { bắtChạyCụcBộ = chỉSốVòngLặp + 1; break; } }
        else { int sốLượngTổngCộng = 0; for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < sốLượngMục; chỉSốVòngLặp++) if (DữLiệu[chỉSốVòngLặp] == 10 && ++sốLượngTổngCộng == cácDòng) { vịTríKếtThúc = chỉSốVòngLặp + 1; break; } }
        for (int chỉSốVòngLặp = bắtChạyCụcBộ; chỉSốVòngLặp < vịTríKếtThúc; chỉSốVòngLặp++) BoMạch.ghiNốiTiếp(DữLiệu[chỉSốVòngLặp]);
    }
    static void ghiCùng() {
        boolean thêmCuối = TrìnhThôngDịchLệnh.vănBảnBằng(1, "-a"); int chỉSốĐốiSố = thêmCuối ? 2 : 1;
        if (TrìnhThôngDịchLệnh.sốLượngTừTố != chỉSốĐốiSố + 1) { TrìnhThôngDịchLệnh.kếtQuả = 2; VàoRaThiếtBịCuối.ghi("사용법: tee [-a] Tệp\n"); return; }
        int sốTệpĐãMở = mởTệp(chỉSốĐốiSố, thêmCuối ? 1089 : 577); if (sốTệpĐãMở < 0) { TrìnhThôngDịchLệnh.lỗi(sốTệpĐãMở); return; }
        tệpĐầuVào = -1; int dữLiệuByte;
        while ((dữLiệuByte = đọc()) != 256 && dữLiệuByte >= 0) { int giáTrịĐãXửLý = CácTệpBộNhớ.ghi(sốTệpĐãMở, dữLiệuByte); if (giáTrịĐãXửLý < 0) { TrìnhThôngDịchLệnh.lỗi(giáTrịĐãXửLý); break; } BoMạch.ghiNốiTiếp(dữLiệuByte); }
        CácTệpBộNhớ.đóng(sốTệpĐãMở);
    }
}
