// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Kiểm chứng ELF32 trong gói thực thi chỉ đọc, truyền đối số và chạy mỗi lần một tiến trình người dùng. */
public final class QuảnLýThựcThi {
    static final int bắtChạyChươngTrìnhNgườiDùng = 0x04000000;
    static final int kếtThúcNgườiDùng = 0x04400000;
    static final int địaChỉKếtThúcẢnh = 0x04200000;
    static final int bắtChạyĐốiSố = 0x04300000;
    static int sốLượngĐốiSố = 0;
    static int[] địaChỉĐốiSố = new int[16];

    static boolean cắtXén(int địaChỉ, int độDài) {
        return địaChỉ >= bắtChạyChươngTrìnhNgườiDùng && địaChỉ < kếtThúcNgườiDùng && độDài >= 0 && độDài <= kếtThúcNgườiDùng - địaChỉ;
    }

    static int trịSố(int địaChỉ) { return VùngNhớ.phânTíchCúPhápSốNguyên(địaChỉ); }
    static int giáTrịNgắnKiểu(int địaChỉ) { return ThiếtBị.đọcBộNhớ(địaChỉ) | ThiếtBị.đọcBộNhớ(địaChỉ + 1) << 8; }
    static void ghiSố(int địaChỉ, int giáTrị) {
        for (int sốHiệu = 0; sốHiệu < 4; sốHiệu++) ThiếtBị.ghiBộNhớ(địaChỉ + sốHiệu, giáTrị >>> (sốHiệu * 8));
    }

    static int sốLượngNhóm() {
        int địaChỉ = ThiếtBị.GóiGộpTệpThựcThi();
        int cỡ = ThiếtBị.cỡGóiGộpTệpThựcThi();
        if (cỡ < 8 || trịSố(địaChỉ) != 0x50414b4a) return 0;
        int sốLượngPhầnMục = trịSố(địaChỉ + 4);
        return sốLượngPhầnMục >= 0 && sốLượngPhầnMục <= 32 && sốLượngPhầnMục <= (cỡ - 8) / 24 ? sốLượngPhầnMục : 0;
    }

    static void danhSáchMục() {
        for (int sốHiệu = 0; sốHiệu < sốLượngNhóm(); sốHiệu++) {
            int giáTrịMục = ThiếtBị.GóiGộpTệpThựcThi() + 8 + sốHiệu * 24;
            for (int giáTrịKýTự = 0; giáTrịKýTự < 16 && ThiếtBị.đọcBộNhớ(giáTrịMục + giáTrịKýTự) != 0; giáTrịKýTự++)
                ĐầuCuốiVănBản.KýTự(ThiếtBị.đọcBộNhớ(giáTrịMục + giáTrịKýTự));
            ĐầuCuốiVănBản.ghi("\n");
        }
    }

    static int tìmMục(int[] giáTrịVào, int chạy, int độDài) {
        if (độDài <= 0 || độDài >= 16) return 0;
        for (int sốHiệu = 0; sốHiệu < sốLượngNhóm(); sốHiệu++) {
            int giáTrịMục = ThiếtBị.GóiGộpTệpThựcThi() + 8 + sốHiệu * 24;
            boolean vănBảnBằng = ThiếtBị.đọcBộNhớ(giáTrịMục + độDài) == 0;
            for (int giáTrịKýTự = 0; giáTrịKýTự < độDài; giáTrịKýTự++)
                if (giáTrịVào[chạy + giáTrịKýTự] != ThiếtBị.đọcBộNhớ(giáTrịMục + giáTrịKýTự)) vănBảnBằng = false;
            if (vănBảnBằng) return giáTrịMục;
        }
        return 0;
    }

    static int thẩmĐịnh(int Tệp, int độDài) {
        if (độDài < 52 || trịSố(Tệp) != 0x464c457f || ThiếtBị.đọcBộNhớ(Tệp + 4) != 1
            || ThiếtBị.đọcBộNhớ(Tệp + 5) != 1 || ThiếtBị.đọcBộNhớ(Tệp + 6) != 1
            || giáTrịNgắnKiểu(Tệp + 16) != 2 || giáTrịNgắnKiểu(Tệp + 18) != 3 || trịSố(Tệp + 20) != 1
            || giáTrịNgắnKiểu(Tệp + 40) != 52 || giáTrịNgắnKiểu(Tệp + 42) != 32) return -8;
        int giáTrịĐiểmMục = trịSố(Tệp + 24);
        int vịTríBảngTra = trịSố(Tệp + 28);
        int sốLượngPhầnMục = giáTrịNgắnKiểu(Tệp + 44);
        if (sốLượngPhầnMục == 0 || sốLượngPhầnMục > 16 || vịTríBảngTra < 52 || vịTríBảngTra > độDài - sốLượngPhầnMục * 32) return -8;
        boolean làTệpThựcThi = false;
        for (int sốHiệu = 0; sốHiệu < sốLượngPhầnMục; sốHiệu++) {
            int Bảng = Tệp + vịTríBảngTra + sốHiệu * 32;
            int giáTrịLoại = trịSố(Bảng);
            if (giáTrịLoại == 2 || giáTrịLoại == 3) return -8; // Không hỗ trợ liên kết động hay trình thông dịch.
            if (giáTrịLoại != 1) continue;
            int vịTrí = trịSố(Bảng + 4), địaChỉ = trịSố(Bảng + 8), cỡTệp = trịSố(Bảng + 16), cỡBộNhớ = trịSố(Bảng + 20);
            int giáTrịCănChỉnh = trịSố(Bảng + 28);
            if (địaChỉ < bắtChạyChươngTrìnhNgườiDùng || địaChỉ >= địaChỉKếtThúcẢnh || cỡBộNhớ < 0 || cỡBộNhớ > địaChỉKếtThúcẢnh - địaChỉ
                || cỡTệp < 0 || cỡTệp > cỡBộNhớ || vịTrí < 0 || (cỡTệp > 0 && vịTrí > độDài - cỡTệp)
                || (giáTrịCănChỉnh != 0 && (giáTrịCănChỉnh < 0 || (giáTrịCănChỉnh & (giáTrịCănChỉnh - 1)) != 0
                    || ((địaChỉ - vịTrí) & (giáTrịCănChỉnh - 1)) != 0))) return -8;
            for (int giáTrịPhíaTrước = 0; giáTrịPhíaTrước < sốHiệu; giáTrịPhíaTrước++) {
                int phầnMụcTrướcĐó = Tệp + vịTríBảngTra + giáTrịPhíaTrước * 32;
                if (trịSố(phầnMụcTrướcĐó) == 1 && cỡBộNhớ > 0 && trịSố(phầnMụcTrướcĐó + 20) > 0
                    && địaChỉ < trịSố(phầnMụcTrướcĐó + 8) + trịSố(phầnMụcTrướcĐó + 20) && trịSố(phầnMụcTrướcĐó + 8) < địaChỉ + cỡBộNhớ) return -8;
            }
            if ((trịSố(Bảng + 24) & 1) != 0 && giáTrịĐiểmMục >= địaChỉ && giáTrịĐiểmMục - địaChỉ < cỡTệp) làTệpThựcThi = true;
        }
        return làTệpThựcThi ? giáTrịĐiểmMục : -8;
    }

    static int thựcThiLệnh(int[] giáTrịVào, int chạy, int độDài) {
        while (chạy < độDài && giáTrịVào[chạy] == ' ') chạy++;
        int phầnKết = chạy;
        while (phầnKết < độDài && giáTrịVào[phầnKết] != ' ') phầnKết++;
        int giáTrịMục = tìmMục(giáTrịVào, chạy, phầnKết - chạy);
        if (giáTrịMục == 0) return -2;
        int vịTrí = trịSố(giáTrịMục + 16), cỡ = trịSố(giáTrịMục + 20);
        if (vịTrí < 8 + sốLượngNhóm() * 24 || cỡ < 52 || vịTrí > ThiếtBị.cỡGóiGộpTệpThựcThi() - cỡ) return -8;
        int Tệp = ThiếtBị.GóiGộpTệpThựcThi() + vịTrí;
        int giáTrịĐiểmMục = thẩmĐịnh(Tệp, cỡ);
        if (giáTrịĐiểmMục < 0) return giáTrịĐiểmMục;
        ThiếtBị.cácNộiDungXóaSạchNgườiDùng();
        int vịTríBảngTra = trịSố(Tệp + 28), sốLượngPhầnMục = giáTrịNgắnKiểu(Tệp + 44);
        for (int sốHiệu = 0; sốHiệu < sốLượngPhầnMục; sốHiệu++) {
            int Bảng = Tệp + vịTríBảngTra + sốHiệu * 32;
            if (trịSố(Bảng) != 1) continue;
            int nguyênBản = Tệp + trịSố(Bảng + 4), giáTrịĐích = trịSố(Bảng + 8), cỡTệp = trịSố(Bảng + 16);
            for (int giáTrịByte = 0; giáTrịByte < cỡTệp; giáTrịByte++) ThiếtBị.ghiBộNhớ(giáTrịĐích + giáTrịByte, ThiếtBị.đọcBộNhớ(nguyênBản + giáTrịByte));
        }
        sốLượngĐốiSố = 0;
        int giáTrịCất = bắtChạyĐốiSố;
        while (phầnKết < độDài) {
            while (phầnKết < độDài && giáTrịVào[phầnKết] == ' ') phầnKết++;
            if (phầnKết == độDài) break;
            if (sốLượngĐốiSố == địaChỉĐốiSố.length) return -22;
            chạy = phầnKết;
            while (phầnKết < độDài && giáTrịVào[phầnKết] != ' ') phầnKết++;
            địaChỉĐốiSố[sốLượngĐốiSố++] = giáTrịCất;
            ghiSố(giáTrịCất, phầnKết - chạy);
            for (int giáTrịKýTự = chạy; giáTrịKýTự < phầnKết; giáTrịKýTự++) ghiSố(giáTrịCất + 4 + (giáTrịKýTự - chạy) * 4, giáTrịVào[giáTrịKýTự]);
            giáTrịCất += 4 + (phầnKết - chạy) * 4;
        }
        NgănXếpMạng.tiếnTrìnhSạch();
        QuảnLýMôTảTệp.bắtChạyTiếnTrình();
        int kếtQuả = ThiếtBị.chạyChươngTrìnhNgườiDùng(giáTrịĐiểmMục, kếtThúcNgườiDùng - 16);
        QuảnLýMôTảTệp.tiếnTrìnhSạch();
        NgănXếpMạng.tiếnTrìnhSạch();
        return kếtQuả;
    }
}
