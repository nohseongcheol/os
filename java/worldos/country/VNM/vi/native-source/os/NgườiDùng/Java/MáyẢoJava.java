// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** JVM giới hạn chạy ở ring 3. Kiểm tra giới hạn tệp, ngăn xếp, tham chiếu và nhánh khi thực thi. */
public final class MáyẢoJava {
    static int[] Tệp = new int[16384], vănBảnTênTệp = new int[64];
    static int[] thẻHằng = new int[512], giáTrịĐầuTiênHằng = new int[512], giáTrịThứHaiHằng = new int[512], thamChiếuChuỗi = new int[512];
    static int[] vănBảnTênPhươngThức = new int[32], kiểuPhươngThức = new int[32], truyCậpPhươngThức = new int[32];
    static int[] bắtChạyPhươngThức = new int[32], kếtThúcPhươngThức = new int[32], ngănXếpPhươngThức = new int[32], cácBiếnCụcBộPhươngThức = new int[32];
    static int[] sốLượngĐốiSốPhươngThức = new int[32], kiểuĐốiSốPhươngThức = new int[512], trảVềPhươngThức = new int[32];
    static int[] giáTrịRanhGiới = new int[16384];
    static int[] giáTrịCụcBộ = new int[4096], kiểuCụcBộ = new int[4096], giáTrịNgănXếpToánHạng = new int[4096], kiểuNgănXếpToánHạng = new int[4096];
    static int[] phươngThứcKhung = new int[32], vịTríKhung = new int[32], ngănXếpKhung = new int[32];
    static int[] giáTrịVùngNhớĐộng = new int[8192];
    static int cỡ, đọcVịTrí, sốLượngHằng, sốLượngPhươngThức, tênLớp, chỉSốKhung = -1, vịTríKếtThúcVùngNhớĐộng = 1, kiểuTrảVề;
    static boolean lỗi;

    static void giáTrịSựThấtBại(String vănBảnTừ) {
        if (!lỗi) { NgườiDùng.ghi("JVM error: "); NgườiDùng.ghi(vănBảnTừ); NgườiDùng.ghiGiáTrịKýTự(10); }
        lỗi = true;
    }
    static boolean cắtXén(int chạy, int độDài) { return chạy >= 0 && độDài >= 0 && chạy <= cỡ - độDài; }
    static int giáTrịByte() {
        if (!cắtXén(đọcVịTrí, 1)) { giáTrịSựThấtBại("truncated class file"); return 0; }
        return Tệp[đọcVịTrí++];
    }
    static int giáTrịNgắnKiểu() { return giáTrịByte() << 8 | giáTrịByte(); }
    static int SốNguyên() { return giáTrịNgắnKiểu() << 16 | giáTrịNgắnKiểu(); }
    static void bỏBướcCácByte(int độDài) { if (!cắtXén(đọcVịTrí, độDài)) giáTrịSựThấtBại("invalid attribute size"); else đọcVịTrí += độDài; }
    static boolean kiểmTraHằng(int trịSố, int giáTrịLoại) {
        if (trịSố <= 0 || trịSố >= sốLượngHằng || thẻHằng[trịSố] != giáTrịLoại) { giáTrịSựThấtBại("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean khoảngVănBản(int chạy, int độDài, String vănBảnTừ) {
        if (!cắtXén(chạy, độDài) || độDài != vănBảnTừ.length()) return false;
        for (int trịSố = 0; trịSố < độDài; trịSố++) if (Tệp[chạy + trịSố] != vănBảnTừ.charAt(trịSố)) return false;
        return true;
    }
    static boolean vănBảnTừ(int giáTrịHằng, String vănBảnTừ) { return kiểmTraHằng(giáTrịHằng, 1) && khoảngVănBản(giáTrịĐầuTiênHằng[giáTrịHằng], giáTrịThứHaiHằng[giáTrịHằng], vănBảnTừ); }
    static boolean từViệcSoKhớp(int toánHạngĐầuTiên, int toánHạngThứHai) {
        if (!kiểmTraHằng(toánHạngĐầuTiên, 1) || !kiểmTraHằng(toánHạngThứHai, 1) || giáTrịThứHaiHằng[toánHạngĐầuTiên] != giáTrịThứHaiHằng[toánHạngThứHai]) return false;
        for (int trịSố = 0; trịSố < giáTrịThứHaiHằng[toánHạngĐầuTiên]; trịSố++) if (Tệp[giáTrịĐầuTiênHằng[toánHạngĐầuTiên] + trịSố] != Tệp[giáTrịĐầuTiênHằng[toánHạngThứHai] + trịSố]) return false;
        return true;
    }
    static int vănBảnTênLớp(int trịSố) { return kiểmTraHằng(trịSố, 7) && kiểmTraHằng(giáTrịĐầuTiênHằng[trịSố], 1) ? giáTrịĐầuTiênHằng[trịSố] : 0; }
    static int tênThamChiếu(int trịSố) { return kiểmTraHằng(trịSố, 12) && kiểmTraHằng(giáTrịĐầuTiênHằng[trịSố], 1) ? giáTrịĐầuTiênHằng[trịSố] : 0; }
    static int kiểuThamChiếu(int trịSố) { return kiểmTraHằng(trịSố, 12) && kiểmTraHằng(giáTrịThứHaiHằng[trịSố], 1) ? giáTrịThứHaiHằng[trịSố] : 0; }
    static int kiểuBộMôTả(int phầnKết, boolean kiểuRỗng) {
        if (đọcVịTrí >= phầnKết) { giáTrịSựThấtBại("invalid descriptor"); return 0; }
        int giáTrị = giáTrịByte();
        if (giáTrị == 'V' && kiểuRỗng) return 0;
        if (giáTrị == 'I' || giáTrị == 'B' || giáTrị == 'C' || giáTrị == 'S' || giáTrị == 'Z') return 1;
        if (giáTrị == '[') { kiểuBộMôTả(phầnKết, false); return 2; }
        if (giáTrị == 'L') {
            int chạy = đọcVịTrí;
            while (đọcVịTrí < phầnKết && Tệp[đọcVịTrí] != ';') đọcVịTrí++;
            if (đọcVịTrí == phầnKết || đọcVịTrí == chạy) giáTrịSựThấtBại("invalid reference descriptor");
            else đọcVịTrí++;
            return 2;
        }
        giáTrịSựThấtBại("unsupported descriptor type"); return 0;
    }
    static void đọcBộMôTả(int Hàm) {
        int phầnMụcTrướcĐó = đọcVịTrí, trịSố = kiểuPhươngThức[Hàm];
        if (!kiểmTraHằng(trịSố, 1)) return;
        đọcVịTrí = giáTrịĐầuTiênHằng[trịSố]; int phầnKết = đọcVịTrí + giáTrịThứHaiHằng[trịSố];
        if (giáTrịByte() != '(') giáTrịSựThấtBại("invalid method descriptor");
        int sốLượngPhầnMục = 0;
        while (!lỗi && đọcVịTrí < phầnKết && Tệp[đọcVịTrí] != ')') {
            if (sốLượngPhầnMục == 16) { giáTrịSựThấtBại("too many method arguments"); break; }
            kiểuĐốiSốPhươngThức[Hàm * 16 + sốLượngPhầnMục++] = kiểuBộMôTả(phầnKết, false);
        }
        if (đọcVịTrí >= phầnKết || giáTrịByte() != ')') giáTrịSựThấtBại("invalid method descriptor");
        trảVềPhươngThức[Hàm] = kiểuBộMôTả(phầnKết, true); sốLượngĐốiSốPhươngThức[Hàm] = sốLượngPhầnMục;
        if (đọcVịTrí != phầnKết) giáTrịSựThấtBại("invalid method descriptor");
        đọcVịTrí = phầnMụcTrướcĐó;
    }
    static void bỏBướcThuộcTính() {
        int sốLượngPhầnMục = giáTrịNgắnKiểu();
        for (int trịSố = 0; trịSố < sốLượngPhầnMục && !lỗi; trịSố++) { kiểmTraHằng(giáTrịNgắnKiểu(), 1); bỏBướcCácByte(SốNguyên()); }
    }
    static int độDàiLệnh(int giáTrị) {
        if (giáTrị == 16 || giáTrị == 18 || giáTrị == 21 || giáTrị == 25 || giáTrị == 54 || giáTrị == 58 || giáTrị == 188) return 2;
        if (giáTrị == 17 || giáTrị == 19 || giáTrị == 132 || giáTrị >= 153 && giáTrị <= 167
            || giáTrị >= 178 && giáTrị <= 184 || giáTrị == 187 || giáTrị == 189 || giáTrị == 192 || giáTrị == 198 || giáTrị == 199) return 3;
        if (giáTrị >= 0 && giáTrị <= 8 || giáTrị >= 26 && giáTrị <= 29 || giáTrị >= 42 && giáTrị <= 46 || giáTrị == 50
            || giáTrị >= 59 && giáTrị <= 62 || giáTrị >= 75 && giáTrị <= 79 || giáTrị == 83 || giáTrị == 87 || giáTrị == 89 || giáTrị == 95
            || giáTrị == 96 || giáTrị == 100 || giáTrị == 104 || giáTrị == 108 || giáTrị == 112 || giáTrị == 116
            || giáTrị == 120 || giáTrị == 122 || giáTrị == 124 || giáTrị == 126 || giáTrị == 128 || giáTrị == 130
            || giáTrị >= 145 && giáTrị <= 147 || giáTrị == 172 || giáTrị == 176 || giáTrị == 177 || giáTrị == 190) return 1;
        return 0;
    }
    static void đọcLớp() {
        if (SốNguyên() != 0xcafebabe) giáTrịSựThấtBại("not a class file");
        int bảnSửaThứYếu = giáTrịNgắnKiểu(), giáTrịPhiênBản = giáTrịNgắnKiểu();
        if (giáTrịPhiênBản < 45 || giáTrịPhiênBản > 52 || bảnSửaThứYếu != 0) giáTrịSựThấtBại("supported class versions: 45..52, minor 0");
        sốLượngHằng = giáTrịNgắnKiểu();
        if (sốLượngHằng < 1 || sốLượngHằng > 512) { giáTrịSựThấtBại("constant pool limit (511)"); return; }
        for (int trịSố = 1; trịSố < sốLượngHằng && !lỗi; trịSố++) {
            int giáTrịLoại = giáTrịByte(); thẻHằng[trịSố] = giáTrịLoại;
            if (giáTrịLoại == 1) { giáTrịThứHaiHằng[trịSố] = giáTrịNgắnKiểu(); giáTrịĐầuTiênHằng[trịSố] = đọcVịTrí; bỏBướcCácByte(giáTrịThứHaiHằng[trịSố]); }
            else if (giáTrịLoại == 3) giáTrịĐầuTiênHằng[trịSố] = SốNguyên();
            else if (giáTrịLoại == 7 || giáTrịLoại == 8) giáTrịĐầuTiênHằng[trịSố] = giáTrịNgắnKiểu();
            else if (giáTrịLoại == 9 || giáTrịLoại == 10 || giáTrịLoại == 12) { giáTrịĐầuTiênHằng[trịSố] = giáTrịNgắnKiểu(); giáTrịThứHaiHằng[trịSố] = giáTrịNgắnKiểu(); }
            else giáTrịSựThấtBại("unsupported constant type");
        }
        int giáTrịQuyền = giáTrịNgắnKiểu();
        if ((giáTrịQuyền & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) giáTrịSựThấtBại("unsupported class flags");
        tênLớp = vănBảnTênLớp(giáTrịNgắnKiểu());
        if (!vănBảnTừ(vănBảnTênLớp(giáTrịNgắnKiểu()), "java/lang/Object")) giáTrịSựThấtBại("inheritance unsupported");
        if (giáTrịNgắnKiểu() != 0) giáTrịSựThấtBại("interfaces unsupported");
        if (giáTrịNgắnKiểu() != 0) giáTrịSựThấtBại("fields unsupported");
        sốLượngPhươngThức = giáTrịNgắnKiểu();
        if (sốLượngPhươngThức < 1 || sốLượngPhươngThức > 32) { giáTrịSựThấtBại("method count limit (32)"); return; }
        for (int trịSố = 0; trịSố < sốLượngPhươngThức && !lỗi; trịSố++) {
            truyCậpPhươngThức[trịSố] = giáTrịNgắnKiểu(); vănBảnTênPhươngThức[trịSố] = giáTrịNgắnKiểu(); kiểuPhươngThức[trịSố] = giáTrịNgắnKiểu();
            kiểmTraHằng(vănBảnTênPhươngThức[trịSố], 1); đọcBộMôTả(trịSố);
            if ((truyCậpPhươngThức[trịSố] & (0x100 | 0x400 | 0x20)) != 0) giáTrịSựThấtBại("native, abstract and synchronized methods unsupported");
            if ((truyCậpPhươngThức[trịSố] & 8) == 0 && !vănBảnTừ(vănBảnTênPhươngThức[trịSố], "<init>")) giáTrịSựThấtBại("instance methods unsupported");
            if (vănBảnTừ(vănBảnTênPhươngThức[trịSố], "<clinit>")) giáTrịSựThấtBại("class initializers unsupported");
            for (int giáTrịPhíaTrước = 0; giáTrịPhíaTrước < trịSố; giáTrịPhíaTrước++) if (từViệcSoKhớp(vănBảnTênPhươngThức[giáTrịPhíaTrước], vănBảnTênPhươngThức[trịSố]) && từViệcSoKhớp(kiểuPhươngThức[giáTrịPhíaTrước], kiểuPhươngThức[trịSố])) giáTrịSựThấtBại("duplicate method");
            int sốLượngPhầnMục = giáTrịNgắnKiểu();
            for (int giáTrịThuộcTính = 0; giáTrịThuộcTính < sốLượngPhầnMục && !lỗi; giáTrịThuộcTính++) {
                int tên = giáTrịNgắnKiểu(), độDài = SốNguyên(), chạy = đọcVịTrí;
                if (!cắtXén(chạy, độDài)) { giáTrịSựThấtBại("truncated method attribute"); break; }
                if (vănBảnTừ(tên, "Code")) {
                    if (bắtChạyPhươngThức[trịSố] != 0) giáTrịSựThấtBại("duplicate Code attribute");
                    ngănXếpPhươngThức[trịSố] = giáTrịNgắnKiểu(); cácBiếnCụcBộPhươngThức[trịSố] = giáTrịNgắnKiểu(); int độDàiMã = SốNguyên();
                    if (ngănXếpPhươngThức[trịSố] > 128 || cácBiếnCụcBộPhươngThức[trịSố] > 128 || cácBiếnCụcBộPhươngThức[trịSố] < sốLượngĐốiSốPhươngThức[trịSố]
                        || độDàiMã < 1 || độDàiMã > 8192) giáTrịSựThấtBại("method memory limits exceeded");
                    bắtChạyPhươngThức[trịSố] = đọcVịTrí; bỏBướcCácByte(độDàiMã); kếtThúcPhươngThức[trịSố] = đọcVịTrí;
                    if (giáTrịNgắnKiểu() != 0) giáTrịSựThấtBại("exception handlers unsupported");
                    bỏBướcThuộcTính();
                    if (đọcVịTrí != chạy + độDài) giáTrịSựThấtBại("Code attribute size mismatch");
                } else bỏBướcCácByte(độDài);
            }
            if (bắtChạyPhươngThức[trịSố] == 0) giáTrịSựThấtBại("missing Code attribute");
            int mụcÔ = bắtChạyPhươngThức[trịSố];
            while (mụcÔ < kếtThúcPhươngThức[trịSố] && !lỗi) {
                int độDài = độDàiLệnh(Tệp[mụcÔ]);
                if (độDài == 0 || độDài > kếtThúcPhươngThức[trịSố] - mụcÔ) { giáTrịSựThấtBại("unsupported or truncated bytecode"); break; }
                giáTrịRanhGiới[mụcÔ] = trịSố + 1; mụcÔ += độDài;
            }
            // Từ chối đích nhánh sai ngay cả trên đường không bao giờ được chạy.
            mụcÔ = bắtChạyPhươngThức[trịSố];
            while (mụcÔ < kếtThúcPhươngThức[trịSố] && !lỗi) {
                int giáTrị = Tệp[mụcÔ];
                if (giáTrị >= 153 && giáTrị <= 167 || giáTrị == 198 || giáTrị == 199) {
                    int giáTrịĐích = mụcÔ + (short)(Tệp[mụcÔ + 1] << 8 | Tệp[mụcÔ + 2]);
                    if (giáTrịĐích < bắtChạyPhươngThức[trịSố] || giáTrịĐích >= kếtThúcPhươngThức[trịSố] || giáTrịRanhGiới[giáTrịĐích] != trịSố + 1) giáTrịSựThấtBại("invalid branch target");
                }
                mụcÔ += độDàiLệnh(giáTrị);
            }
        }
        if (!lỗi) bỏBướcThuộcTính();
        if (đọcVịTrí != cỡ) giáTrịSựThấtBại("extra class file data");
    }
    static int cấpPhátLưuTrữ(int giáTrịLoại, int độDài) {
        if (độDài < 0 || độDài > giáTrịVùngNhớĐộng.length - vịTríKếtThúcVùngNhớĐộng - 2) { giáTrịSựThấtBại("object heap exhausted or negative array size"); return 0; }
        int thamChiếu = vịTríKếtThúcVùngNhớĐộng; vịTríKếtThúcVùngNhớĐộng += độDài + 2; giáTrịVùngNhớĐộng[thamChiếu] = giáTrịLoại; giáTrịVùngNhớĐộng[thamChiếu + 1] = độDài;
        return thamChiếu;
    }
    static boolean giáTrịĐốiTượng(int thamChiếu, int giáTrịLoại) {
        if (thamChiếu < 1 || thamChiếu >= vịTríKếtThúcVùngNhớĐộng - 1 || giáTrịVùngNhớĐộng[thamChiếu] != giáTrịLoại) { giáTrịSựThấtBại("null or invalid object reference"); return false; }
        return true;
    }
    static int vănBảnHằng(int sốHiệu) {
        if (!kiểmTraHằng(sốHiệu, 1)) return 0;
        if (thamChiếuChuỗi[sốHiệu] != 0) return thamChiếuChuỗi[sốHiệu];
        int thamChiếu = cấpPhátLưuTrữ(1, giáTrịThứHaiHằng[sốHiệu]); if (lỗi) return 0;
        int phầnKết = giáTrịĐầuTiênHằng[sốHiệu] + giáTrịThứHaiHằng[sốHiệu], trịSố = giáTrịĐầuTiênHằng[sốHiệu], độDài = 0;
        while (trịSố < phầnKết && !lỗi) {
            int giáTrị = Tệp[trịSố++];
            if (giáTrị == 0) giáTrịSựThấtBại("invalid modified UTF-8");
            else if (giáTrị >= 192 && giáTrị <= 223 && trịSố < phầnKết) {
                int phầnMụcKếTiếp = Tệp[trịSố++];
                if ((phầnMụcKếTiếp & 192) != 128) giáTrịSựThấtBại("invalid modified UTF-8");
                giáTrị = (giáTrị & 31) << 6 | phầnMụcKếTiếp & 63;
                if (giáTrị != 0 && giáTrị < 128) giáTrịSựThấtBại("overlong modified UTF-8");
            } else if (giáTrị >= 224 && giáTrị <= 239 && trịSố + 1 < phầnKết) {
                int toánHạngĐầuTiên = Tệp[trịSố++], toánHạngThứHai = Tệp[trịSố++];
                if ((toánHạngĐầuTiên & 192) != 128 || (toánHạngThứHai & 192) != 128) giáTrịSựThấtBại("invalid modified UTF-8");
                giáTrị = (giáTrị & 15) << 12 | (toánHạngĐầuTiên & 63) << 6 | toánHạngThứHai & 63;
                if (giáTrị < 2048) giáTrịSựThấtBại("overlong modified UTF-8");
            } else if (giáTrị >= 128) giáTrịSựThấtBại("invalid modified UTF-8");
            giáTrịVùngNhớĐộng[thamChiếu + 2 + độDài++] = giáTrị;
        }
        giáTrịVùngNhớĐộng[thamChiếu + 1] = độDài; thamChiếuChuỗi[sốHiệu] = thamChiếu; return thamChiếu;
    }
    static int kýTựChủ(String giáTrị) {
        int thamChiếu = cấpPhátLưuTrữ(1, giáTrị.length()); if (lỗi) return 0;
        for (int trịSố = 0; trịSố < giáTrị.length(); trịSố++) giáTrịVùngNhớĐộng[thamChiếu + 2 + trịSố] = giáTrị.charAt(trịSố);
        return thamChiếu;
    }
    static void ghiVănBản(int thamChiếu) {
        if (thamChiếu == 0) { NgườiDùng.ghi("null"); return; }
        if (!giáTrịĐốiTượng(thamChiếu, 1)) return;
        for (int trịSố = 0; trịSố < giáTrịVùngNhớĐộng[thamChiếu + 1]; trịSố++) NgườiDùng.ghiGiáTrịKýTự(giáTrịVùngNhớĐộng[thamChiếu + 2 + trịSố]);
    }
    static int kýTựChữSố(int giáTrị) {
        int thamChiếu = cấpPhátLưuTrữ(1, 11); if (lỗi) return 0;
        int độDài = 0;
        if (giáTrị < 0) giáTrịVùngNhớĐộng[thamChiếu + 2 + độDài++] = '-'; else giáTrị = -giáTrị;
        int chỉSốVịTrí = 1000000000; boolean chạy = false;
        while (chỉSốVịTrí != 0) {
            int trịSố = -(giáTrị / chỉSốVịTrí);
            if (trịSố != 0 || chạy || chỉSốVịTrí == 1) { giáTrịVùngNhớĐộng[thamChiếu + 2 + độDài++] = '0' + trịSố; chạy = true; }
            giáTrị %= chỉSốVịTrí; chỉSốVịTrí /= 10;
        }
        giáTrịVùngNhớĐộng[thamChiếu + 1] = độDài; return thamChiếu;
    }
    static int giảiMãSốNguyên(int thamChiếu) {
        if (!giáTrịĐốiTượng(thamChiếu, 1)) return 0;
        int độDài = giáTrịVùngNhớĐộng[thamChiếu + 1], trịSố = 0, giáTrị = 0; boolean giáTrịÂm = false;
        if (độDài > 0 && (giáTrịVùngNhớĐộng[thamChiếu + 2] == '-' || giáTrịVùngNhớĐộng[thamChiếu + 2] == '+')) { giáTrịÂm = giáTrịVùngNhớĐộng[thamChiếu + 2] == '-'; trịSố++; }
        if (trịSố == độDài) giáTrịSựThấtBại("NumberFormatException");
        for (; trịSố < độDài && !lỗi; trịSố++) {
            int giáTrịChữSố = giáTrịVùngNhớĐộng[thamChiếu + 2 + trịSố] - '0';
            if (giáTrịChữSố < 0 || giáTrịChữSố > 9 || giáTrị < -214748364 || giáTrị == -214748364 && giáTrịChữSố > (giáTrịÂm ? 8 : 7)) giáTrịSựThấtBại("NumberFormatException");
            giáTrị = giáTrị * 10 - giáTrịChữSố;
        }
        return giáTrịÂm ? giáTrị : -giáTrị;
    }
    static void đặtGiáTrị(int giáTrị, int giáTrịKiểu) {
        if (lỗi) return;
        if (chỉSốKhung < 0 || ngănXếpKhung[chỉSốKhung] >= ngănXếpPhươngThức[phươngThứcKhung[chỉSốKhung]]) { giáTrịSựThấtBại("operand stack overflow"); return; }
        int mụcÔ = chỉSốKhung * 128 + ngănXếpKhung[chỉSốKhung]++; giáTrịNgănXếpToánHạng[mụcÔ] = giáTrị; kiểuNgănXếpToánHạng[mụcÔ] = giáTrịKiểu;
    }
    static int trừCácGiáTrị(int giáTrịKiểu) {
        if (lỗi) return 0;
        if (chỉSốKhung < 0 || ngănXếpKhung[chỉSốKhung] < 1) { giáTrịSựThấtBại("operand stack underflow"); return 0; }
        int mụcÔ = chỉSốKhung * 128 + --ngănXếpKhung[chỉSốKhung]; kiểuTrảVề = kiểuNgănXếpToánHạng[mụcÔ];
        if (giáTrịKiểu != 0 && kiểuTrảVề != giáTrịKiểu) giáTrịSựThấtBại("operand type mismatch");
        return giáTrịNgănXếpToánHạng[mụcÔ];
    }
    static void đọcCụcBộ(int sốHiệu, int giáTrịKiểu) {
        if (sốHiệu >= cácBiếnCụcBộPhươngThức[phươngThứcKhung[chỉSốKhung]] || sốHiệu < 0 || kiểuCụcBộ[chỉSốKhung * 128 + sốHiệu] != giáTrịKiểu) { giáTrịSựThấtBại("invalid or uninitialized local"); return; }
        đặtGiáTrị(giáTrịCụcBộ[chỉSốKhung * 128 + sốHiệu], giáTrịKiểu);
    }
    static void ghiCụcBộ(int sốHiệu, int giáTrịKiểu) {
        if (sốHiệu >= cácBiếnCụcBộPhươngThức[phươngThứcKhung[chỉSốKhung]] || sốHiệu < 0) { giáTrịSựThấtBại("local index out of range"); return; }
        int giáTrị = trừCácGiáTrị(giáTrịKiểu); giáTrịCụcBộ[chỉSốKhung * 128 + sốHiệu] = giáTrị; kiểuCụcBộ[chỉSốKhung * 128 + sốHiệu] = giáTrịKiểu;
    }
    static int đọcByteMãThaoTác() {
        int vịTrí = vịTríKhung[chỉSốKhung];
        if (vịTrí < bắtChạyPhươngThức[phươngThứcKhung[chỉSốKhung]] || vịTrí >= kếtThúcPhươngThức[phươngThứcKhung[chỉSốKhung]]) { giáTrịSựThấtBại("instruction pointer out of range"); return 0; }
        vịTríKhung[chỉSốKhung]++; return Tệp[vịTrí];
    }
    static int đọcNgắnKiểuMãThaoTác() { return đọcByteMãThaoTác() << 8 | đọcByteMãThaoTác(); }
    static void giáTrịDiChuyển(int vịTrí) {
        int Hàm = phươngThứcKhung[chỉSốKhung];
        if (vịTrí < bắtChạyPhươngThức[Hàm] || vịTrí >= kếtThúcPhươngThức[Hàm] || giáTrịRanhGiới[vịTrí] != Hàm + 1) giáTrịSựThấtBại("invalid branch target");
        else vịTríKhung[chỉSốKhung] = vịTrí;
    }
    static void gọiThựcHiện(int Hàm) {
        if (chỉSốKhung == 31) { giáTrịSựThấtBại("call stack limit (32)"); return; }
        int phầnMụcKếTiếp = chỉSốKhung + 1;
        for (int trịSố = 0; trịSố < 128; trịSố++) kiểuCụcBộ[phầnMụcKếTiếp * 128 + trịSố] = 0;
        for (int trịSố = sốLượngĐốiSốPhươngThức[Hàm] - 1; trịSố >= 0; trịSố--) {
            giáTrịCụcBộ[phầnMụcKếTiếp * 128 + trịSố] = trừCácGiáTrị(kiểuĐốiSốPhươngThức[Hàm * 16 + trịSố]); kiểuCụcBộ[phầnMụcKếTiếp * 128 + trịSố] = kiểuĐốiSốPhươngThức[Hàm * 16 + trịSố];
        }
        chỉSốKhung = phầnMụcKếTiếp; phươngThứcKhung[chỉSốKhung] = Hàm; vịTríKhung[chỉSốKhung] = bắtChạyPhươngThức[Hàm]; ngănXếpKhung[chỉSốKhung] = 0;
    }
    static void kếtQuảTrảVề(int giáTrịKiểu) {
        if (giáTrịKiểu != trảVềPhươngThức[phươngThứcKhung[chỉSốKhung]]) { giáTrịSựThấtBại("return type mismatch"); return; }
        int giáTrị = giáTrịKiểu == 0 ? 0 : trừCácGiáTrị(giáTrịKiểu);
        chỉSốKhung--; if (chỉSốKhung >= 0 && giáTrịKiểu != 0) đặtGiáTrị(giáTrị, giáTrịKiểu);
    }
    static int[] tênTệpLuồng = new int[64];
    static void gọiLuồngTệp(int giáTrịChủSởHữu, int tên, int giáTrịĐịnhDạng, int lệnh) {
        boolean ĐầuRa = vănBảnTừ(giáTrịChủSởHữu, "java/io/FileOutputStream");
        int giáTrịLoại = ĐầuRa ? 6 : 5;
        if (lệnh == 183 && vănBảnTừ(tên, "<init>")) {
            boolean giáTrịSựTiếpDiễn = false;
            if (ĐầuRa && vănBảnTừ(giáTrịĐịnhDạng, "(Ljava/lang/String;Z)V")) giáTrịSựTiếpDiễn = trừCácGiáTrị(1) != 0;
            else if (!vănBảnTừ(giáTrịĐịnhDạng, "(Ljava/lang/String;)V")) { giáTrịSựThấtBại("unsupported file stream constructor"); return; }
            int tênMụcTệp = trừCácGiáTrị(2), giáTrịLuồng = trừCácGiáTrị(2);
            if (!giáTrịĐốiTượng(tênMụcTệp, 1) || !giáTrịĐốiTượng(giáTrịLuồng, giáTrịLoại) || lỗi) return;
            if (giáTrịVùngNhớĐộng[giáTrịLuồng + 3] != 0) { giáTrịSựThấtBại("file stream already initialized"); return; }
            int độDài = giáTrịVùngNhớĐộng[tênMụcTệp + 1];
            if (độDài < 1 || độDài > 63) { giáTrịSựThấtBại("invalid file name length"); return; }
            for (int mụcÔ = 0; mụcÔ < độDài; mụcÔ++) {
                int giáTrị = giáTrịVùngNhớĐộng[tênMụcTệp + 2 + mụcÔ];
                if (giáTrị < 1 || giáTrị > 127) { giáTrịSựThấtBại("file stream paths currently require ASCII"); return; }
                tênTệpLuồng[mụcÔ] = giáTrị;
            }
            tênTệpLuồng[độDài] = 0;
            int mụcBộMôTả = NgườiDùng.mởBộMôTảTệp(tênTệpLuồng, ĐầuRa ? (giáTrịSựTiếpDiễn ? 1089 : 577) : 0);
            if (mụcBộMôTả < 0) { giáTrịSựThấtBại("FileNotFoundException: file open failed"); return; }
            giáTrịVùngNhớĐộng[giáTrịLuồng + 2] = mụcBộMôTả; giáTrịVùngNhớĐộng[giáTrịLuồng + 3] = 1;
            return;
        }
        if (lệnh != 182) { giáTrịSựThấtBại("invalid file stream invocation"); return; }
        int hànhĐộng = -1, giáTrị = 0;
        if (vănBảnTừ(tên, "close") && vănBảnTừ(giáTrịĐịnhDạng, "()V")) hànhĐộng = 0;
        if (!ĐầuRa && vănBảnTừ(tên, "read") && vănBảnTừ(giáTrịĐịnhDạng, "()I")) hànhĐộng = 1;
        if (ĐầuRa && vănBảnTừ(tên, "write") && vănBảnTừ(giáTrịĐịnhDạng, "(I)V")) { hànhĐộng = 2; giáTrị = trừCácGiáTrị(1); }
        if (hànhĐộng < 0) { giáTrịSựThấtBại("unsupported file stream method"); return; }
        int giáTrịLuồng = trừCácGiáTrị(2);
        if (!giáTrịĐốiTượng(giáTrịLuồng, giáTrịLoại) || lỗi) return;
        if (giáTrịVùngNhớĐộng[giáTrịLuồng + 3] == 0) { giáTrịSựThấtBại("uninitialized file stream"); return; }
        int mụcBộMôTả = giáTrịVùngNhớĐộng[giáTrịLuồng + 2];
        if (hànhĐộng == 0) {
            if (mụcBộMôTả >= 0 && NgườiDùng.đóngBộMôTảTệp(mụcBộMôTả) < 0) giáTrịSựThấtBại("IOException: close failed");
            giáTrịVùngNhớĐộng[giáTrịLuồng + 2] = -1; return;
        }
        if (mụcBộMôTả < 0) { giáTrịSựThấtBại("IOException: stream closed"); return; }
        if (hànhĐộng == 1) {
            int kếtQuả = NgườiDùng.đọcByteTệpMột(mụcBộMôTả);
            if (kếtQuả < -1) giáTrịSựThấtBại("IOException: read failed"); else đặtGiáTrị(kếtQuả, 1);
        } else if (NgườiDùng.ghiByteTệpMột(mụcBộMôTả, giáTrị) != 1) giáTrịSựThấtBại("IOException: write failed");
    }
    static void gọiPhươngThức(int sốHiệu, int lệnh) {
        if (!kiểmTraHằng(sốHiệu, 10)) return;
        int giáTrịChủSởHữu = vănBảnTênLớp(giáTrịĐầuTiênHằng[sốHiệu]), tên = tênThamChiếu(giáTrịThứHaiHằng[sốHiệu]), giáTrịĐịnhDạng = kiểuThamChiếu(giáTrịThứHaiHằng[sốHiệu]);
        if (lỗi) return;
        if (từViệcSoKhớp(giáTrịChủSởHữu, tênLớp)) {
            if (lệnh != 184) { giáTrịSựThấtBại("only static user methods are supported"); return; }
            for (int trịSố = 0; trịSố < sốLượngPhươngThức; trịSố++) if (từViệcSoKhớp(tên, vănBảnTênPhươngThức[trịSố]) && từViệcSoKhớp(giáTrịĐịnhDạng, kiểuPhươngThức[trịSố])) {
                if ((truyCậpPhươngThức[trịSố] & 8) == 0) giáTrịSựThấtBại("method is not static"); else gọiThựcHiện(trịSố);
                return;
            }
            giáTrịSựThấtBại("NoSuchMethodError"); return;
        }
        if (vănBảnTừ(giáTrịChủSởHữu, "java/io/FileInputStream") || vănBảnTừ(giáTrịChủSởHữu, "java/io/FileOutputStream")) {
            gọiLuồngTệp(giáTrịChủSởHữu, tên, giáTrịĐịnhDạng, lệnh); return;
        }
        if (lệnh == 184 && vănBảnTừ(giáTrịChủSởHữu, "java/lang/Integer") && vănBảnTừ(tên, "parseInt") && vănBảnTừ(giáTrịĐịnhDạng, "(Ljava/lang/String;)I")) {
            đặtGiáTrị(giảiMãSốNguyên(trừCácGiáTrị(2)), 1); return;
        }
        if (lệnh == 182 && vănBảnTừ(giáTrịChủSởHữu, "java/io/PrintStream") && (vănBảnTừ(tên, "println") || vănBảnTừ(tên, "print"))) {
            int giáTrịKiểu = 0, giáTrị = 0;
            if (vănBảnTừ(giáTrịĐịnhDạng, "(I)V")) { giáTrịKiểu = 1; giáTrị = trừCácGiáTrị(1); }
            else if (vănBảnTừ(giáTrịĐịnhDạng, "(Z)V")) { giáTrịKiểu = 2; giáTrị = trừCácGiáTrị(1); }
            else if (vănBảnTừ(giáTrịĐịnhDạng, "(C)V")) { giáTrịKiểu = 3; giáTrị = trừCácGiáTrị(1); }
            else if (vănBảnTừ(giáTrịĐịnhDạng, "(Ljava/lang/String;)V")) { giáTrịKiểu = 4; giáTrị = trừCácGiáTrị(2); }
            else if (!vănBảnTừ(giáTrịĐịnhDạng, "()V") || !vănBảnTừ(tên, "println")) giáTrịSựThấtBại("unsupported print descriptor");
            if (trừCácGiáTrị(2) != -1) giáTrịSựThấtBại("invalid PrintStream receiver");
            if (lỗi) return;
            if (giáTrịKiểu == 1) CôngCụJava.ghiSố(giáTrị);
            if (giáTrịKiểu == 2) NgườiDùng.ghi(giáTrị == 0 ? "false" : "true");
            if (giáTrịKiểu == 3) NgườiDùng.ghiGiáTrịKýTự(giáTrị & 65535);
            if (giáTrịKiểu == 4) ghiVănBản(giáTrị);
            if (vănBảnTừ(tên, "println")) NgườiDùng.ghiGiáTrịKýTự(10);
            return;
        }
        if (lệnh == 182 && vănBảnTừ(giáTrịChủSởHữu, "java/lang/String")) {
            if (vănBảnTừ(tên, "length") && vănBảnTừ(giáTrịĐịnhDạng, "()I")) {
                int thamChiếu = trừCácGiáTrị(2); if (giáTrịĐốiTượng(thamChiếu, 1)) đặtGiáTrị(giáTrịVùngNhớĐộng[thamChiếu + 1], 1); return;
            }
            if (vănBảnTừ(tên, "charAt") && vănBảnTừ(giáTrịĐịnhDạng, "(I)C")) {
                int giáTrịChỉSốDưới = trừCácGiáTrị(1), thamChiếu = trừCácGiáTrị(2);
                if (giáTrịĐốiTượng(thamChiếu, 1)) {
                    if (giáTrịChỉSốDưới < 0 || giáTrịChỉSốDưới >= giáTrịVùngNhớĐộng[thamChiếu + 1]) giáTrịSựThấtBại("StringIndexOutOfBoundsException"); else đặtGiáTrị(giáTrịVùngNhớĐộng[thamChiếu + 2 + giáTrịChỉSốDưới], 1);
                }
                return;
            }
        }
        if (vănBảnTừ(giáTrịChủSởHữu, "java/lang/StringBuilder")) {
            if (lệnh == 183 && vănBảnTừ(tên, "<init>") && vănBảnTừ(giáTrịĐịnhDạng, "()V")) { giáTrịĐốiTượng(trừCácGiáTrị(2), 4); return; }
            if (lệnh == 182 && vănBảnTừ(tên, "toString") && vănBảnTừ(giáTrịĐịnhDạng, "()Ljava/lang/String;")) {
                int thamChiếu = trừCácGiáTrị(2); if (giáTrịĐốiTượng(thamChiếu, 4)) đặtGiáTrị(giáTrịVùngNhớĐộng[thamChiếu + 2] == 0 ? kýTựChủ("") : giáTrịVùngNhớĐộng[thamChiếu + 2], 2); return;
            }
            if (lệnh == 182 && vănBảnTừ(tên, "append")) {
                int vănBản = 0;
                if (vănBảnTừ(giáTrịĐịnhDạng, "(I)Ljava/lang/StringBuilder;")) vănBản = kýTựChữSố(trừCácGiáTrị(1));
                else if (vănBảnTừ(giáTrịĐịnhDạng, "(Z)Ljava/lang/StringBuilder;")) vănBản = kýTựChủ(trừCácGiáTrị(1) == 0 ? "false" : "true");
                else if (vănBảnTừ(giáTrịĐịnhDạng, "(C)Ljava/lang/StringBuilder;")) {
                    int giáTrị = trừCácGiáTrị(1); vănBản = cấpPhátLưuTrữ(1, 1); if (!lỗi) giáTrịVùngNhớĐộng[vănBản + 2] = giáTrị & 65535;
                }
                else if (vănBảnTừ(giáTrịĐịnhDạng, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { vănBản = trừCácGiáTrị(2); if (vănBản == 0) vănBản = kýTựChủ("null"); }
                else { giáTrịSựThấtBại("unsupported StringBuilder append"); return; }
                int thamChiếu = trừCácGiáTrị(2); if (!giáTrịĐốiTượng(thamChiếu, 4) || !giáTrịĐốiTượng(vănBản, 1)) return;
                int giáTrịPhíaTrước = giáTrịVùngNhớĐộng[thamChiếu + 2], độDàiGiáTrịPhíaTrước = giáTrịPhíaTrước == 0 ? 0 : giáTrịVùngNhớĐộng[giáTrịPhíaTrước + 1], độDàiGiáTrịLùi = giáTrịVùngNhớĐộng[vănBản + 1];
                int vănBảnMới = cấpPhátLưuTrữ(1, độDàiGiáTrịPhíaTrước + độDàiGiáTrịLùi); if (lỗi) return;
                for (int trịSố = 0; trịSố < độDàiGiáTrịPhíaTrước; trịSố++) giáTrịVùngNhớĐộng[vănBảnMới + 2 + trịSố] = giáTrịVùngNhớĐộng[giáTrịPhíaTrước + 2 + trịSố];
                for (int trịSố = 0; trịSố < độDàiGiáTrịLùi; trịSố++) giáTrịVùngNhớĐộng[vănBảnMới + 2 + độDàiGiáTrịPhíaTrước + trịSố] = giáTrịVùngNhớĐộng[vănBản + 2 + trịSố];
                giáTrịVùngNhớĐộng[thamChiếu + 2] = vănBảnMới; đặtGiáTrị(thamChiếu, 2); return;
            }
        }
        giáTrịSựThấtBại("unsupported library method");
    }
    static int ôMảng(int thamChiếu, int giáTrịChỉSốDưới, int giáTrịKiểu) {
        if (!giáTrịĐốiTượng(thamChiếu, giáTrịKiểu)) return 0;
        if (giáTrịChỉSốDưới < 0 || giáTrịChỉSốDưới >= giáTrịVùngNhớĐộng[thamChiếu + 1]) { giáTrịSựThấtBại("ArrayIndexOutOfBoundsException"); return 0; }
        return thamChiếu + 2 + giáTrịChỉSốDưới;
    }
    static void thựcThiLệnh() {
        int dữLiệuSốDư = 500000;
        while (chỉSốKhung >= 0 && !lỗi) {
            if (--dữLiệuSốDư == 0) { giáTrịSựThấtBại("instruction limit (500000)"); break; }
            int chạy = vịTríKhung[chỉSốKhung], giáTrị = đọcByteMãThaoTác();
            if (lỗi) break;
            if (giáTrị == 0) continue;
            if (giáTrị == 1) { đặtGiáTrị(0, 2); continue; }
            if (giáTrị >= 2 && giáTrị <= 8) { đặtGiáTrị(giáTrị - 3, 1); continue; }
            if (giáTrị == 16) { đặtGiáTrị((byte)đọcByteMãThaoTác(), 1); continue; }
            if (giáTrị == 17) { đặtGiáTrị((short)đọcNgắnKiểuMãThaoTác(), 1); continue; }
            if (giáTrị == 18 || giáTrị == 19) {
                int trịSố = giáTrị == 18 ? đọcByteMãThaoTác() : đọcNgắnKiểuMãThaoTác();
                if (trịSố <= 0 || trịSố >= sốLượngHằng) giáTrịSựThấtBại("invalid ldc constant");
                else if (thẻHằng[trịSố] == 3) đặtGiáTrị(giáTrịĐầuTiênHằng[trịSố], 1);
                else if (thẻHằng[trịSố] == 8) đặtGiáTrị(vănBảnHằng(giáTrịĐầuTiênHằng[trịSố]), 2);
                else giáTrịSựThấtBại("unsupported ldc constant");
                continue;
            }
            if (giáTrị == 21 || giáTrị == 25) { đọcCụcBộ(đọcByteMãThaoTác(), giáTrị == 21 ? 1 : 2); continue; }
            if (giáTrị >= 26 && giáTrị <= 29) { đọcCụcBộ(giáTrị - 26, 1); continue; }
            if (giáTrị >= 42 && giáTrị <= 45) { đọcCụcBộ(giáTrị - 42, 2); continue; }
            if (giáTrị == 54 || giáTrị == 58) { ghiCụcBộ(đọcByteMãThaoTác(), giáTrị == 54 ? 1 : 2); continue; }
            if (giáTrị >= 59 && giáTrị <= 62) { ghiCụcBộ(giáTrị - 59, 1); continue; }
            if (giáTrị >= 75 && giáTrị <= 78) { ghiCụcBộ(giáTrị - 75, 2); continue; }
            if (giáTrị == 46 || giáTrị == 50) {
                int giáTrịChỉSốDưới = trừCácGiáTrị(1), thamChiếu = trừCácGiáTrị(2), mụcÔ = ôMảng(thamChiếu, giáTrịChỉSốDưới, giáTrị == 46 ? 2 : 3);
                if (!lỗi) đặtGiáTrị(giáTrịVùngNhớĐộng[mụcÔ], giáTrị == 46 ? 1 : 2); continue;
            }
            if (giáTrị == 79 || giáTrị == 83) {
                int phầnTửPhầnMục = trừCácGiáTrị(giáTrị == 79 ? 1 : 2), giáTrịChỉSốDưới = trừCácGiáTrị(1), thamChiếu = trừCácGiáTrị(2), mụcÔ = ôMảng(thamChiếu, giáTrịChỉSốDưới, giáTrị == 79 ? 2 : 3);
                if (giáTrị == 83 && phầnTửPhầnMục != 0) giáTrịĐốiTượng(phầnTửPhầnMục, 1);
                if (!lỗi) giáTrịVùngNhớĐộng[mụcÔ] = phầnTửPhầnMục; continue;
            }
            if (giáTrị == 87) { trừCácGiáTrị(0); continue; }
            if (giáTrị == 89) { int toánHạngĐầuTiên = trừCácGiáTrị(0), giáTrịKiểu = kiểuTrảVề; đặtGiáTrị(toánHạngĐầuTiên, giáTrịKiểu); đặtGiáTrị(toánHạngĐầuTiên, giáTrịKiểu); continue; }
            if (giáTrị == 95) { int toánHạngĐầuTiên = trừCácGiáTrị(0), kiểuToánHạngĐầuTiên = kiểuTrảVề, toánHạngThứHai = trừCácGiáTrị(0), kiểuToánHạngThứHai = kiểuTrảVề; đặtGiáTrị(toánHạngĐầuTiên, kiểuToánHạngĐầuTiên); đặtGiáTrị(toánHạngThứHai, kiểuToánHạngThứHai); continue; }
            if (giáTrị == 96 || giáTrị == 100 || giáTrị == 104 || giáTrị == 108 || giáTrị == 112 || giáTrị == 120
                || giáTrị == 122 || giáTrị == 124 || giáTrị == 126 || giáTrị == 128 || giáTrị == 130) {
                int toánHạngThứHai = trừCácGiáTrị(1), toánHạngĐầuTiên = trừCácGiáTrị(1), kếtQuả = 0;
                if ((giáTrị == 108 || giáTrị == 112) && toánHạngThứHai == 0) { giáTrịSựThấtBại("ArithmeticException: / by zero"); continue; }
                if (giáTrị == 96) kếtQuả = toánHạngĐầuTiên + toánHạngThứHai;
                if (giáTrị == 100) kếtQuả = toánHạngĐầuTiên - toánHạngThứHai;
                if (giáTrị == 104) kếtQuả = toánHạngĐầuTiên * toánHạngThứHai;
                if (giáTrị == 108) kếtQuả = toánHạngĐầuTiên / toánHạngThứHai;
                if (giáTrị == 112) kếtQuả = toánHạngĐầuTiên % toánHạngThứHai;
                if (giáTrị == 120) kếtQuả = toánHạngĐầuTiên << toánHạngThứHai;
                if (giáTrị == 122) kếtQuả = toánHạngĐầuTiên >> toánHạngThứHai;
                if (giáTrị == 124) kếtQuả = toánHạngĐầuTiên >>> toánHạngThứHai;
                if (giáTrị == 126) kếtQuả = toánHạngĐầuTiên & toánHạngThứHai;
                if (giáTrị == 128) kếtQuả = toánHạngĐầuTiên | toánHạngThứHai;
                if (giáTrị == 130) kếtQuả = toánHạngĐầuTiên ^ toánHạngThứHai;
                đặtGiáTrị(kếtQuả, 1); continue;
            }
            if (giáTrị == 116) { đặtGiáTrị(-trừCácGiáTrị(1), 1); continue; }
            if (giáTrị == 132) {
                int phạmViCụcBộ = đọcByteMãThaoTác(), bướcBướcTăng = (byte)đọcByteMãThaoTác(); đọcCụcBộ(phạmViCụcBộ, 1); đặtGiáTrị(trừCácGiáTrị(1) + bướcBướcTăng, 1); ghiCụcBộ(phạmViCụcBộ, 1); continue;
            }
            if (giáTrị >= 145 && giáTrị <= 147) {
                int trịSố = trừCácGiáTrị(1); đặtGiáTrị(giáTrị == 145 ? (byte)trịSố : giáTrị == 146 ? (char)trịSố : (short)trịSố, 1); continue;
            }
            if (giáTrị >= 153 && giáTrị <= 167 || giáTrị == 198 || giáTrị == 199) {
                int giáTrịĐích = chạy + (short)đọcNgắnKiểuMãThaoTác(); boolean nênTiếnHành = giáTrị == 167;
                if (giáTrị >= 153 && giáTrị <= 158) {
                    int trịSố = trừCácGiáTrị(1); nênTiếnHành = giáTrị == 153 ? trịSố == 0 : giáTrị == 154 ? trịSố != 0 : giáTrị == 155 ? trịSố < 0 : giáTrị == 156 ? trịSố >= 0 : giáTrị == 157 ? trịSố > 0 : trịSố <= 0;
                } else if (giáTrị >= 159 && giáTrị <= 166) {
                    int toánHạngThứHai = trừCácGiáTrị(giáTrị >= 165 ? 2 : 1), toánHạngĐầuTiên = trừCácGiáTrị(giáTrị >= 165 ? 2 : 1);
                    nênTiếnHành = giáTrị == 159 || giáTrị == 165 ? toánHạngĐầuTiên == toánHạngThứHai : giáTrị == 160 || giáTrị == 166 ? toánHạngĐầuTiên != toánHạngThứHai : giáTrị == 161 ? toánHạngĐầuTiên < toánHạngThứHai : giáTrị == 162 ? toánHạngĐầuTiên >= toánHạngThứHai : giáTrị == 163 ? toánHạngĐầuTiên > toánHạngThứHai : toánHạngĐầuTiên <= toánHạngThứHai;
                } else if (giáTrị == 198 || giáTrị == 199) { int trịSố = trừCácGiáTrị(2); nênTiếnHành = giáTrị == 198 ? trịSố == 0 : trịSố != 0; }
                if (nênTiếnHành) giáTrịDiChuyển(giáTrịĐích); continue;
            }
            if (giáTrị == 172 || giáTrị == 176 || giáTrị == 177) { kếtQuảTrảVề(giáTrị == 172 ? 1 : giáTrị == 176 ? 2 : 0); continue; }
            if (giáTrị == 178) {
                int trịSố = đọcNgắnKiểuMãThaoTác(); if (!kiểmTraHằng(trịSố, 9)) continue;
                if (!vănBảnTừ(vănBảnTênLớp(giáTrịĐầuTiênHằng[trịSố]), "java/lang/System") || !vănBảnTừ(tênThamChiếu(giáTrịThứHaiHằng[trịSố]), "out")
                    || !vănBảnTừ(kiểuThamChiếu(giáTrịThứHaiHằng[trịSố]), "Ljava/io/PrintStream;")) giáTrịSựThấtBại("unsupported static field");
                else đặtGiáTrị(-1, 2); continue;
            }
            if (giáTrị == 182 || giáTrị == 183 || giáTrị == 184) { gọiPhươngThức(đọcNgắnKiểuMãThaoTác(), giáTrị); continue; }
            if (giáTrị == 187) {
                int tên = vănBảnTênLớp(đọcNgắnKiểuMãThaoTác());
                if (vănBảnTừ(tên, "java/lang/StringBuilder")) đặtGiáTrị(cấpPhátLưuTrữ(4, 1), 2);
                else if (vănBảnTừ(tên, "java/io/FileInputStream") || vănBảnTừ(tên, "java/io/FileOutputStream")) {
                    int thamChiếu = cấpPhátLưuTrữ(vănBảnTừ(tên, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!lỗi) { giáTrịVùngNhớĐộng[thamChiếu + 2] = -1; đặtGiáTrị(thamChiếu, 2); }
                } else giáTrịSựThấtBại("unsupported object construction");
                continue;
            }
            if (giáTrị == 188 || giáTrị == 189) {
                if (giáTrị == 188) { if (đọcByteMãThaoTác() != 10) giáTrịSựThấtBại("only int[] newarray is supported"); }
                else if (!vănBảnTừ(vănBảnTênLớp(đọcNgắnKiểuMãThaoTác()), "java/lang/String")) giáTrịSựThấtBại("only String[] anewarray is supported");
                int độDài = trừCácGiáTrị(1); đặtGiáTrị(cấpPhátLưuTrữ(giáTrị == 188 ? 2 : 3, độDài), 2); continue;
            }
            if (giáTrị == 190) {
                int thamChiếu = trừCácGiáTrị(2);
                if (thamChiếu < 1 || thamChiếu >= vịTríKếtThúcVùngNhớĐộng - 1 || (giáTrịVùngNhớĐộng[thamChiếu] != 2 && giáTrịVùngNhớĐộng[thamChiếu] != 3)) giáTrịSựThấtBại("null or invalid array");
                else đặtGiáTrị(giáTrịVùngNhớĐộng[thamChiếu + 1], 1); continue;
            }
            if (giáTrị == 192) {
                int tên = vănBảnTênLớp(đọcNgắnKiểuMãThaoTác()), thamChiếu = trừCácGiáTrị(2);
                if (!vănBảnTừ(tên, "java/lang/String")) giáTrịSựThấtBại("unsupported checkcast");
                else if (thamChiếu != 0) giáTrịĐốiTượng(thamChiếu, 1);
                đặtGiáTrị(thamChiếu, 2); continue;
            }
            giáTrịSựThấtBại("unsupported bytecode");
        }
    }
    public static int chạy() {
        if (NgườiDùng.sốLượngCácĐốiSố() == 1 && CôngCụJava.vănBảnBằng(NgườiDùng.cácĐốiSố(0), "-version")) {
            NgườiDùng.ghi("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (NgườiDùng.sốLượngCácĐốiSố() < 1) { NgườiDùng.ghi("Usage: java CLASS [ARGS]\n"); return 2; }
        int độDài = CôngCụJava.tên(vănBảnTênTệp, NgườiDùng.cácĐốiSố(0));
        if (độDài < 1 || độDài > 57) { NgườiDùng.ghi("java: invalid class name\n"); return 2; }
        vănBảnTênTệp[độDài] = '.'; vănBảnTênTệp[độDài + 1] = 'c'; vănBảnTênTệp[độDài + 2] = 'l'; vănBảnTênTệp[độDài + 3] = 'a'; vănBảnTênTệp[độDài + 4] = 's'; vănBảnTênTệp[độDài + 5] = 's';
        cỡ = NgườiDùng.đọcTệp(vănBảnTênTệp, Tệp);
        if (cỡ < 0) { NgườiDùng.ghi("java: cannot read class: "); CôngCụJava.ghiSố(cỡ); NgườiDùng.ghiGiáTrịKýTự(10); return 1; }
        đọcLớp(); if (lỗi) return 1;
        int tênKýTự = vănBảnHằng(tênLớp);
        if (!lỗi && giáTrịVùngNhớĐộng[tênKýTự + 1] != độDài) giáTrịSựThấtBại("class name does not match file");
        for (int trịSố = 0; trịSố < độDài && !lỗi; trịSố++) if (giáTrịVùngNhớĐộng[tênKýTự + 2 + trịSố] != vănBảnTênTệp[trịSố]) giáTrịSựThấtBại("class name does not match file");
        int giáTrịĐiểmMục = -1;
        for (int trịSố = 0; trịSố < sốLượngPhươngThức; trịSố++) if (vănBảnTừ(vănBảnTênPhươngThức[trịSố], "main") && vănBảnTừ(kiểuPhươngThức[trịSố], "([Ljava/lang/String;)V") && (truyCậpPhươngThức[trịSố] & 9) == 9) giáTrịĐiểmMục = trịSố;
        if (giáTrịĐiểmMục < 0) giáTrịSựThấtBại("public static void main(String[] args) required");
        if (lỗi) return 1;
        int cácĐốiSố = cấpPhátLưuTrữ(3, NgườiDùng.sốLượngCácĐốiSố() - 1);
        for (int trịSố = 1; trịSố < NgườiDùng.sốLượngCácĐốiSố() && !lỗi; trịSố++) giáTrịVùngNhớĐộng[cácĐốiSố + 1 + trịSố] = kýTựChủ(NgườiDùng.cácĐốiSố(trịSố));
        chỉSốKhung = 0; phươngThứcKhung[0] = giáTrịĐiểmMục; vịTríKhung[0] = bắtChạyPhươngThức[giáTrịĐiểmMục]; giáTrịCụcBộ[0] = cácĐốiSố; kiểuCụcBộ[0] = 2;
        thựcThiLệnh(); return lỗi ? 1 : 0;
    }
}
