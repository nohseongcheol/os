// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Trạng thái trình thông dịch lệnh cho bốn thiết bị cuối. Dùng chung kho tệp nhưng tách đường dẫn, biến, lịch sử và đầu vào. */
public final class phiênCửaSổ {
    static int[] giữNguyênGiáTrị = new int[4 * 30000], chuẩnBị = new int[4];
    static int phầnMụcHiệnTại, vịTrí;
    static boolean đọcSựTiếpDiễn;
    static void giáTrịMảng(int[] DữLiệu, boolean giáTrịCất) {
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < DữLiệu.length; chỉSốVòngLặp++) { if (giáTrịCất) giữNguyênGiáTrị[vịTrí++] = DữLiệu[chỉSốVòngLặp]; else DữLiệu[chỉSốVòngLặp] = giữNguyênGiáTrị[vịTrí++]; }
    }
    static int giáTrị(int giáTrịDữLiệu, boolean đãCấtĐãLà) { if (đãCấtĐãLà) { giữNguyênGiáTrị[vịTrí++] = giáTrịDữLiệu; return giáTrịDữLiệu; } return giữNguyênGiáTrị[vịTrí++]; }
    static void dịchVịVịTrí(int ôĐãGiữNguyên, boolean đãCấtĐãLà) {
        vịTrí = ôĐãGiữNguyên * 30000;
        giáTrịMảng(CácTệpBộNhớ.phầnMụcHiệnTại, đãCấtĐãLà); CácTệpBộNhớ.độDàiHiệnTại = giáTrị(CácTệpBộNhớ.độDàiHiệnTại, đãCấtĐãLà);
        giáTrịMảng(CúPhápVỏLệnh.tênBiến, đãCấtĐãLà); giáTrịMảng(CúPhápVỏLệnh.dữLiệuBiến, đãCấtĐãLà); giáTrịMảng(CúPhápVỏLệnh.độDàiTên, đãCấtĐãLà); giáTrịMảng(CúPhápVỏLệnh.độDàiGiáTrị, đãCấtĐãLà);
        CúPhápVỏLệnh.giáTrịTrạngThái = giáTrị(CúPhápVỏLệnh.giáTrịTrạngThái, đãCấtĐãLà);
        giáTrịMảng(TrìnhSoạnThảoDòng.bảnGhiNhậtKý, đãCấtĐãLà); giáTrịMảng(TrìnhSoạnThảoDòng.độDàiNhậtKý, đãCấtĐãLà); giáTrịMảng(TrìnhSoạnThảoDòng.giáTrịCất, đãCấtĐãLà); giáTrịMảng(TrìnhThôngDịchLệnh.dòng, đãCấtĐãLà);
        TrìnhSoạnThảoDòng.sốLượngNhậtKý = giáTrị(TrìnhSoạnThảoDòng.sốLượngNhậtKý, đãCấtĐãLà); TrìnhSoạnThảoDòng.kếtThúcBảnGhiNhậtKý = giáTrị(TrìnhSoạnThảoDòng.kếtThúcBảnGhiNhậtKý, đãCấtĐãLà);
        TrìnhSoạnThảoDòng.tìmKiếmGiáTrị = giáTrị(TrìnhSoạnThảoDòng.tìmKiếmGiáTrị, đãCấtĐãLà); TrìnhSoạnThảoDòng.độDàiĐãCất = giáTrị(TrìnhSoạnThảoDòng.độDàiĐãCất, đãCấtĐãLà);
        TrìnhSoạnThảoDòng.cỡ = giáTrị(TrìnhSoạnThảoDòng.cỡ, đãCấtĐãLà); TrìnhSoạnThảoDòng.giáTrịConTrỏVănBản = giáTrị(TrìnhSoạnThảoDòng.giáTrịConTrỏVănBản, đãCấtĐãLà); TrìnhSoạnThảoDòng.bắtChạyCửaSổ = giáTrị(TrìnhSoạnThảoDòng.bắtChạyCửaSổ, đãCấtĐãLà);
        chuẩnBị[ôĐãGiữNguyên] = 1;
    }
    static void mụcGiáTrịTiếnTrình() {
        int sốSựKiện = BoMạch.thiếtBịCuối(12); if (sốSựKiện == 0) return;
        dịchVịVịTrí(phầnMụcHiệnTại, true);
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < 4; chỉSốVòngLặp++) {
            if ((sốSựKiện & (1 << (8 + chỉSốVòngLặp))) != 0) { BoMạch.chươngTrìnhNgườiDùngĐiềuKhiển(32 + chỉSốVòngLặp); chuẩnBị[chỉSốVòngLặp] = 0; }
            if ((sốSựKiện & (1 << (4 + chỉSốVòngLặp))) != 0 && chỉSốVòngLặp != phầnMụcHiệnTại) chuẩnBị[chỉSốVòngLặp] = 0;
        }
        int vịTríKếTiếp = (sốSựKiện & 15) - 1; if (vịTríKếTiếp < 0) vịTríKếTiếp = 0;
        if (chuẩnBị[vịTríKếTiếp] == 0) for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < 30000; chỉSốVòngLặp++) giữNguyênGiáTrị[vịTríKếTiếp * 30000 + chỉSốVòngLặp] = 0;
        phầnMụcHiệnTại = vịTríKếTiếp; dịchVịVịTrí(phầnMụcHiệnTại, false); BoMạch.thiếtBịCuối(100 + phầnMụcHiệnTại); đọcSựTiếpDiễn = true;
        VàoRaThiếtBịCuối.ghi("\nTERMINAL FOCUS "); VàoRaThiếtBịCuối.trịSố(phầnMụcHiệnTại + 1); VàoRaThiếtBịCuối.KýTự(10);
    }
    static boolean việcThựcThiTiếpDiễn() {
        if (BoMạch.chươngTrìnhNgườiDùngĐiềuKhiển(16 + phầnMụcHiệnTại) == 0) return false;
        VàoRaVỏLệnh.choPhépTươngTác = true; VàoRaVỏLệnh.chạy(false, false); BoMạch.vàoRaChuyển(1);
        int giáTrịĐãXửLý = BoMạch.chươngTrìnhNgườiDùngĐiềuKhiển(phầnMụcHiệnTại); VàoRaVỏLệnh.phầnKết();
        if (giáTrịĐãXửLý != -1005) { đọcSựTiếpDiễn = false; CúPhápVỏLệnh.giáTrịTrạngThái = giáTrịĐãXửLý < 0 ? 126 : giáTrịĐãXửLý; VàoRaThiếtBịCuối.ghi("exit "); VàoRaThiếtBịCuối.trịSố(giáTrịĐãXửLý); VàoRaThiếtBịCuối.KýTự(10); BoMạch.thiếtBịCuối(3); }
        return true;
    }
}
