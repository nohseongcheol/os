// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** JVM giới hạn chạy ở ARM64 EL0. Kiểm tra giới hạn tệp, ngăn xếp, tham chiếu và nhánh khi thực thi. */
public final class MáyẢoJava {
    static int[] Tệp = new int[16 * 16384], tệpTạm = new int[16384], vănBảnTênTệp = new int[512];
    static int[] thẻHằng = new int[8192], giáTrịĐầuTiênHằng = new int[8192], giáTrịThứHaiHằng = new int[8192], thamChiếuChuỗi = new int[8192];
    static int[] vănBảnTênPhươngThức = new int[512], kiểuPhươngThức = new int[512], truyCậpPhươngThức = new int[512], chủSởHữuPhươngThức = new int[512];
    static int[] bắtChạyPhươngThức = new int[512], kếtThúcPhươngThức = new int[512], ngănXếpPhươngThức = new int[512], cácBiếnCụcBộPhươngThức = new int[512];
    static int[] sốLượngĐốiSốPhươngThức = new int[512], kiểuĐốiSốPhươngThức = new int[8192], trảVềPhươngThức = new int[512];
    static int[] giáTrịRanhGiới = new int[16 * 16384];
    static int[] giáTrịCụcBộ = new int[16384], kiểuCụcBộ = new int[16384], giáTrịNgănXếpToánHạng = new int[16384], kiểuNgănXếpToánHạng = new int[16384];
    static int[] phươngThứcKhung = new int[128], vịTríKhung = new int[128], ngănXếpKhung = new int[128], chỉLệnhKhung = new int[128], khởiTạoKhung = new int[128];
    static int[] tênĐịnhNghĩaLớp = new int[16], cỡĐịnhNghĩaLớp = new int[16], chaĐịnhNghĩaLớp = new int[16], trạngTháiĐịnhNghĩaLớp = new int[16], sốLượngÔLớp = new int[16], khởiTạoĐịnhNghĩaLớp = new int[16];
    static int[] giaoDiệnLớp = new int[16 * 16], sốLượngGiaoDiệnLớp = new int[16];
    static int[] tênÔ = new int[512], kiểuÔ = new int[512], chủSởHữuÔ = new int[512], cácQuyềnÔ = new int[512], vịTríÔ = new int[512], dữLiệuÔ = new int[512];
    static int[] bắtBắtChạy = new int[1024], bắtKếtThúc = new int[1024], bắtVịTrí = new int[1024], bắtLớp = new int[1024], bắtPhươngThức = new int[1024];
    static int[] giáTrịVùngNhớĐộng = new int[32768], rộngVùngNhớĐộng = new int[32768], dấuVùngNhớĐộng = new int[32768], thamChiếuVùngNhớĐộng = new int[32768], chờHiểnThịCho = new int[32768];
    static int[] thamChiếuTạm = new int[256], phầnTửMảng = new int[32768], sốNguyênCất = new int[256];
    static int cỡ, đọcVịTrí, sốLượngPhươngThức, tênLớp, chỉSốKhung = -1, vịTríKếtThúcVùngNhớĐộng = 1, kiểuTrảVề;
    static int sốLượngĐịnhNghĩaLớp, sốLượngÔ, bắtSốLượng, lớpĐãPhânTíchHiệnTại, đốiTượngĐãNém, sốLượngTạm, sốLượngHiểnThị, sốLượngTậpHợp;
    static int luồngChạyHiệnTại, sốLượngLuồngChạy = 1, địnhNghĩaLớpMục;
    static int[] khungLuồngChạy = new int[4], trạngTháiLuồngChạy = new int[4], đốiTượngLuồngChạy = new int[4], đốiĐíchLuồngChạy = new int[4], chờLuồngChạyCho = new int[4];
    static boolean lỗi, đổiYêuCầu;
    static int[] chủSởHữuKhóa = new int[32768], độSâuKhóa = new int[32768], khóaKhung = new int[128], khóaLớp = new int[16], luồngChạyLớp = new int[16];

    static void giáTrịSựThấtBại(String vănBảnTừ) {
        if (lỗi) return;
        int mãLoạiMục = 0;
        if (CôngCụJava.vănBảnBằng(vănBảnTừ, "ArithmeticException: / by zero")) mãLoạiMục = 4;
        if (CôngCụJava.vănBảnBằng(vănBảnTừ, "NullPointerException") || CôngCụJava.vănBảnBằng(vănBảnTừ, "null or invalid array")) mãLoạiMục = 5;
        if (CôngCụJava.vănBảnBằng(vănBảnTừ, "ArrayIndexOutOfBoundsException")) mãLoạiMục = 7;
        if (CôngCụJava.vănBảnBằng(vănBảnTừ, "StringIndexOutOfBoundsException")) mãLoạiMục = 8;
        if (CôngCụJava.vănBảnBằng(vănBảnTừ, "NumberFormatException")) mãLoạiMục = 10;
        if (CôngCụJava.vănBảnBằng(vănBảnTừ, "FileNotFoundException: file open failed")) mãLoạiMục = 12;
        if (CôngCụJava.vănBảnBằng(vănBảnTừ, "IOException: stream closed") || CôngCụJava.vănBảnBằng(vănBảnTừ, "IOException: read failed") || CôngCụJava.vănBảnBằng(vănBảnTừ, "IOException: write failed")) mãLoạiMục = 11;
        if (CôngCụJava.vănBảnBằng(vănBảnTừ, "ClassCastException")) mãLoạiMục = 14;
        if (CôngCụJava.vănBảnBằng(vănBảnTừ, "NegativeArraySizeException")) mãLoạiMục = 15;
        if (mãLoạiMục != 0 && chỉSốKhung >= 0) { némNgoạiLệ(mãLoạiMục, vănBảnTừ); return; }
        NgườiDùng.ghi("JVM error: "); NgườiDùng.ghi(vănBảnTừ); NgườiDùng.ghiGiáTrịKýTự(10); lỗi = true;
    }
    static boolean cắtXén(int chạy, int độDài) {
        if (chạy < 0 || chạy >= Tệp.length || độDài < 0) return false;
        int địnhNghĩaLớp = chạy / 16384;
        return chạy % 16384 <= cỡĐịnhNghĩaLớp[địnhNghĩaLớp] && độDài <= cỡĐịnhNghĩaLớp[địnhNghĩaLớp] - chạy % 16384;
    }
    static int giáTrịByte() {
        if (!cắtXén(đọcVịTrí, 1)) { giáTrịSựThấtBại("truncated class file"); return 0; }
        return Tệp[đọcVịTrí++];
    }
    static int giáTrịNgắnKiểu() { return giáTrịByte() << 8 | giáTrịByte(); }
    static int SốNguyên() { return giáTrịNgắnKiểu() << 16 | giáTrịNgắnKiểu(); }
    static void bỏBướcCácByte(int độDài) { if (!cắtXén(đọcVịTrí, độDài)) giáTrịSựThấtBại("invalid attribute size"); else đọcVịTrí += độDài; }
    static boolean kiểmTraHằng(int trịSố, int giáTrịLoại) {
        if (trịSố <= 0 || trịSố >= thẻHằng.length || thẻHằng[trịSố] != giáTrịLoại) { giáTrịSựThấtBại("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean khoảngVănBản(int chạy, int độDài, String vănBảnTừ) {
        if (!cắtXén(chạy, độDài)) return false;
        int đọcConTrỏVănBản = chạy, phầnKết = chạy + độDài;
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < vănBảnTừ.length(); chỉSốVòngLặp++) {
            int mãKýTự = vănBảnTừ.charAt(chỉSốVòngLặp);
            if (mãKýTự > 0 && mãKýTự < 128) { if (đọcConTrỏVănBản >= phầnKết || Tệp[đọcConTrỏVănBản++] != mãKýTự) return false; }
            else if (mãKýTự < 2048) {
                if (đọcConTrỏVănBản + 2 > phầnKết || Tệp[đọcConTrỏVănBản++] != (192 | (mãKýTự >> 6)) || Tệp[đọcConTrỏVănBản++] != (128 | (mãKýTự & 63))) return false;
            } else if (đọcConTrỏVănBản + 3 > phầnKết || Tệp[đọcConTrỏVănBản++] != (224 | (mãKýTự >> 12)) || Tệp[đọcConTrỏVănBản++] != (128 | ((mãKýTự >> 6) & 63)) || Tệp[đọcConTrỏVănBản++] != (128 | (mãKýTự & 63))) return false;
        }
        return đọcConTrỏVănBản == phầnKết;
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
    static int đọcChỉSốHằng() { int giáTrị = giáTrịNgắnKiểu(); return giáTrị == 0 ? 0 : lớpĐãPhânTíchHiệnTại * 512 + giáTrị; }
    static int đọcHằngMãThaoTác() { return chủSởHữuPhươngThức[phươngThứcKhung[chỉSốKhung]] * 512 + đọcNgắnKiểuMãThaoTác(); }
    static void bỏBướcThuộcTính() {
        int sốLượngPhầnMục = giáTrịNgắnKiểu();
        for (int trịSố = 0; trịSố < sốLượngPhầnMục && !lỗi; trịSố++) { kiểmTraHằng(đọcChỉSốHằng(), 1); bỏBướcCácByte(SốNguyên()); }
    }
    static int độDàiLệnh(int giáTrị) {
        if (giáTrị == 16 || giáTrị == 18 || giáTrị == 21 || giáTrị == 25 || giáTrị == 54 || giáTrị == 58 || giáTrị == 188) return 2;
        if (giáTrị == 17 || giáTrị == 19 || giáTrị == 132 || giáTrị >= 153 && giáTrị <= 167
            || giáTrị >= 178 && giáTrị <= 184 || giáTrị == 187 || giáTrị == 189 || giáTrị == 192 || giáTrị == 193 || giáTrị == 198 || giáTrị == 199) return 3;
        if (giáTrị == 185 || giáTrị == 200) return 5;
        if (giáTrị >= 0 && giáTrị <= 8 || giáTrị >= 26 && giáTrị <= 29 || giáTrị >= 42 && giáTrị <= 46 || giáTrị >= 50 && giáTrị <= 53
            || giáTrị >= 59 && giáTrị <= 62 || giáTrị >= 75 && giáTrị <= 79 || giáTrị >= 83 && giáTrị <= 95
            || giáTrị == 96 || giáTrị == 100 || giáTrị == 104 || giáTrị == 108 || giáTrị == 112 || giáTrị == 116
            || giáTrị == 120 || giáTrị == 122 || giáTrị == 124 || giáTrị == 126 || giáTrị == 128 || giáTrị == 130
            || giáTrị >= 145 && giáTrị <= 147 || giáTrị == 172 || giáTrị == 176 || giáTrị == 177 || giáTrị == 190 || giáTrị == 191
            || giáTrị == 194 || giáTrị == 195) return 1;
        return 0;
    }
    static int sốNguyênVịTrí(int đọcConTrỏVănBản) {
        if (!cắtXén(đọcConTrỏVănBản, 4)) { giáTrịSựThấtBại("truncated bytecode operand"); return 0; }
        return Tệp[đọcConTrỏVănBản] << 24 | Tệp[đọcConTrỏVănBản + 1] << 16 | Tệp[đọcConTrỏVănBản + 2] << 8 | Tệp[đọcConTrỏVănBản + 3];
    }
    static int đọcĐộDài(int đọcConTrỏVănBản, int chạy, int phầnKết) {
        int giáTrị = Tệp[đọcConTrỏVănBản], độDài = độDàiLệnh(giáTrị);
        if (giáTrị == 170 || giáTrị == 171) {
            int vịTríCơSở = đọcConTrỏVănBản + 1;
            while ((vịTríCơSở - chạy) % 4 != 0) vịTríCơSở++;
            if (phầnKết - vịTríCơSở < (giáTrị == 170 ? 12 : 8)) return 0;
            int sốLượngMục = giáTrị == 170 ? sốNguyênVịTrí(vịTríCơSở + 8) - sốNguyênVịTrí(vịTríCơSở + 4) + 1 : sốNguyênVịTrí(vịTríCơSở + 4);
            if (sốLượngMục < 0 || sốLượngMục > 2048) return 0;
            độDài = vịTríCơSở - đọcConTrỏVănBản + (giáTrị == 170 ? 12 + 4 * sốLượngMục : 8 + 8 * sốLượngMục);
        }
        if (giáTrị == 196 && đọcConTrỏVănBản + 1 < phầnKết) {
            int dữLiệuTừ = Tệp[đọcConTrỏVănBản + 1]; độDài = dữLiệuTừ == 132 ? 6 : (dữLiệuTừ == 21 || dữLiệuTừ == 25 || dữLiệuTừ == 54 || dữLiệuTừ == 58) ? 4 : 0;
        }
        return độDài > 0 && độDài <= phầnKết - đọcConTrỏVănBản ? độDài : 0;
    }
    static void kiểmTraGiáTrịĐích(int giáTrịĐích, int Hàm) {
        if (giáTrịĐích < bắtChạyPhươngThức[Hàm] || giáTrịĐích >= kếtThúcPhươngThức[Hàm] || giáTrịRanhGiới[giáTrịĐích] != Hàm + 1) giáTrịSựThấtBại("invalid branch target");
    }
    static void đọcLớp(int địnhNghĩaLớp) {
        lớpĐãPhânTíchHiệnTại = địnhNghĩaLớp; đọcVịTrí = địnhNghĩaLớp * 16384; cỡ = đọcVịTrí + cỡĐịnhNghĩaLớp[địnhNghĩaLớp];
        if (SốNguyên() != 0xcafebabe) { giáTrịSựThấtBại("not a class file"); return; }
        int bảnSửaThứYếu = giáTrịNgắnKiểu(), giáTrịPhiênBản = giáTrịNgắnKiểu();
        if (giáTrịPhiênBản < 45 || giáTrịPhiênBản > 52 || bảnSửaThứYếu != 0) { giáTrịSựThấtBại("supported class versions: 45..52, minor 0"); return; }
        int sốLượngHằng = giáTrịNgắnKiểu(), vịTríCơSở = địnhNghĩaLớp * 512;
        if (sốLượngHằng < 1 || sốLượngHằng > 512) { giáTrịSựThấtBại("constant pool limit (511)"); return; }
        for (int sốLượngMục = 1; sốLượngMục < sốLượngHằng && !lỗi; sốLượngMục++) {
            int trịSố = vịTríCơSở + sốLượngMục, giáTrịLoại = giáTrịByte(); thẻHằng[trịSố] = giáTrịLoại;
            if (giáTrịLoại == 1) { giáTrịThứHaiHằng[trịSố] = giáTrịNgắnKiểu(); giáTrịĐầuTiênHằng[trịSố] = đọcVịTrí; bỏBướcCácByte(giáTrịThứHaiHằng[trịSố]); }
            else if (giáTrịLoại == 3) giáTrịĐầuTiênHằng[trịSố] = SốNguyên();
            else if (giáTrịLoại == 7 || giáTrịLoại == 8) giáTrịĐầuTiênHằng[trịSố] = đọcChỉSốHằng();
            else if (giáTrịLoại == 9 || giáTrịLoại == 10 || giáTrịLoại == 11 || giáTrịLoại == 12) { giáTrịĐầuTiênHằng[trịSố] = đọcChỉSốHằng(); giáTrịThứHaiHằng[trịSố] = đọcChỉSốHằng(); }
            else giáTrịSựThấtBại("unsupported constant type");
        }
        int giáTrịQuyền = giáTrịNgắnKiểu();
        if ((giáTrịQuyền & (0x2000 | 0x4000)) != 0) giáTrịSựThấtBại("annotation/enum class unsupported");
        tênĐịnhNghĩaLớp[địnhNghĩaLớp] = vănBảnTênLớp(đọcChỉSốHằng());
        chaĐịnhNghĩaLớp[địnhNghĩaLớp] = vănBảnTênLớp(đọcChỉSốHằng());
        int sốLượngGiaoDiện = giáTrịNgắnKiểu(); if (sốLượngGiaoDiện > 16) { giáTrịSựThấtBại("interface count limit"); return; }
        sốLượngGiaoDiệnLớp[địnhNghĩaLớp] = sốLượngGiaoDiện;
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < sốLượngGiaoDiện; chỉSốVòngLặp++) giaoDiệnLớp[địnhNghĩaLớp * 16 + chỉSốVòngLặp] = vănBảnTênLớp(đọcChỉSốHằng());
        int sốLượngTrường = giáTrịNgắnKiểu();
        if (sốLượngTrường > 512 - sốLượngÔ) { giáTrịSựThấtBại("field count limit (512)"); return; }
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < sốLượngTrường && !lỗi; chỉSốVòngLặp++) {
            int chỉSốTệp = sốLượngÔ++; chủSởHữuÔ[chỉSốTệp] = địnhNghĩaLớp; cácQuyềnÔ[chỉSốTệp] = giáTrịNgắnKiểu(); tênÔ[chỉSốTệp] = đọcChỉSốHằng(); kiểuÔ[chỉSốTệp] = đọcChỉSốHằng();
            kiểmTraHằng(tênÔ[chỉSốTệp], 1); kiểmTraHằng(kiểuÔ[chỉSốTệp], 1);
            int giáTrịĐãGiữNguyên = đọcVịTrí; đọcVịTrí = giáTrịĐầuTiênHằng[kiểuÔ[chỉSốTệp]]; int mãLoạiMục = kiểuBộMôTả(đọcVịTrí + giáTrịThứHaiHằng[kiểuÔ[chỉSốTệp]], false); đọcVịTrí = giáTrịĐãGiữNguyên;
            if ((cácQuyềnÔ[chỉSốTệp] & 8) == 0) vịTríÔ[chỉSốTệp] = sốLượngÔLớp[địnhNghĩaLớp]++;
            int dữLiệuThuộcTính = giáTrịNgắnKiểu();
            for (int vịTríPhíaTrong = 0; vịTríPhíaTrong < dữLiệuThuộcTính && !lỗi; vịTríPhíaTrong++) {
                int hằngTên = đọcChỉSốHằng(), độDàiHợpLệ = SốNguyên();
                if (vănBảnTừ(hằngTên, "ConstantValue") && độDàiHợpLệ == 2) {
                    int giáTrịDữLiệu = đọcChỉSốHằng();
                    if (mãLoạiMục == 1 && kiểmTraHằng(giáTrịDữLiệu, 3)) dữLiệuÔ[chỉSốTệp] = giáTrịĐầuTiênHằng[giáTrịDữLiệu];
                    else if (mãLoạiMục == 2 && kiểmTraHằng(giáTrịDữLiệu, 8)) dữLiệuÔ[chỉSốTệp] = vănBảnHằng(giáTrịĐầuTiênHằng[giáTrịDữLiệu]);
                } else bỏBướcCácByte(độDàiHợpLệ);
            }
        }
        int sốLượngPhầnMục = giáTrịNgắnKiểu();
        if (sốLượngPhầnMục > 512 - sốLượngPhươngThức) { giáTrịSựThấtBại("method count limit (512)"); return; }
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < sốLượngPhầnMục && !lỗi; chỉSốVòngLặp++) {
            int trịSố = sốLượngPhươngThức++; chủSởHữuPhươngThức[trịSố] = địnhNghĩaLớp;
            truyCậpPhươngThức[trịSố] = giáTrịNgắnKiểu(); vănBảnTênPhươngThức[trịSố] = đọcChỉSốHằng(); kiểuPhươngThức[trịSố] = đọcChỉSốHằng();
            kiểmTraHằng(vănBảnTênPhươngThức[trịSố], 1); đọcBộMôTả(trịSố);
            if ((truyCậpPhươngThức[trịSố] & 8) == 0) {
                if (sốLượngĐốiSốPhươngThức[trịSố] == 16) { giáTrịSựThấtBại("too many instance method arguments"); return; }
                for (int vịTríPhépSoSánh = sốLượngĐốiSốPhươngThức[trịSố]; vịTríPhépSoSánh > 0; vịTríPhépSoSánh--) kiểuĐốiSốPhươngThức[trịSố * 16 + vịTríPhépSoSánh] = kiểuĐốiSốPhươngThức[trịSố * 16 + vịTríPhépSoSánh - 1];
                kiểuĐốiSốPhươngThức[trịSố * 16] = 2; sốLượngĐốiSốPhươngThức[trịSố]++;
            }
            if ((truyCậpPhươngThức[trịSố] & 0x100) != 0) giáTrịSựThấtBại("user native method unsupported");
            if (vănBảnTừ(vănBảnTênPhươngThức[trịSố], "<clinit>")) khởiTạoĐịnhNghĩaLớp[địnhNghĩaLớp] = trịSố + 1;
            for (int giáTrịPhíaTrước = 0; giáTrịPhíaTrước < trịSố; giáTrịPhíaTrước++) if (chủSởHữuPhươngThức[giáTrịPhíaTrước] == địnhNghĩaLớp && từViệcSoKhớp(vănBảnTênPhươngThức[giáTrịPhíaTrước], vănBảnTênPhươngThức[trịSố]) && từViệcSoKhớp(kiểuPhươngThức[giáTrịPhíaTrước], kiểuPhươngThức[trịSố])) giáTrịSựThấtBại("duplicate method");
            int sốLượngThuộcTính = giáTrịNgắnKiểu();
            for (int giáTrịThuộcTính = 0; giáTrịThuộcTính < sốLượngThuộcTính && !lỗi; giáTrịThuộcTính++) {
                int tên = đọcChỉSốHằng(), độDài = SốNguyên(), chạy = đọcVịTrí;
                if (!cắtXén(chạy, độDài)) { giáTrịSựThấtBại("truncated method attribute"); break; }
                if (vănBảnTừ(tên, "Code")) {
                    if (bắtChạyPhươngThức[trịSố] != 0) giáTrịSựThấtBại("duplicate Code attribute");
                    ngănXếpPhươngThức[trịSố] = giáTrịNgắnKiểu(); cácBiếnCụcBộPhươngThức[trịSố] = giáTrịNgắnKiểu(); int độDàiMã = SốNguyên();
                    if (ngănXếpPhươngThức[trịSố] > 128 || cácBiếnCụcBộPhươngThức[trịSố] > 128 || cácBiếnCụcBộPhươngThức[trịSố] < sốLượngĐốiSốPhươngThức[trịSố]
                        || độDàiMã < 1 || độDàiMã > 8192) giáTrịSựThấtBại("method memory limits exceeded");
                    bắtChạyPhươngThức[trịSố] = đọcVịTrí; bỏBướcCácByte(độDàiMã); kếtThúcPhươngThức[trịSố] = đọcVịTrí;
                    int sốLượngĐangBắt = giáTrịNgắnKiểu();
                    if (sốLượngĐangBắt > 1024 - bắtSốLượng) { giáTrịSựThấtBại("exception table limit"); return; }
                    for (int vịTríPhíaTrong = 0; vịTríPhíaTrong < sốLượngĐangBắt; vịTríPhíaTrong++) {
                        int thamChiếuLỗi = bắtSốLượng++; bắtPhươngThức[thamChiếuLỗi] = trịSố;
                        bắtBắtChạy[thamChiếuLỗi] = bắtChạyPhươngThức[trịSố] + giáTrịNgắnKiểu(); bắtKếtThúc[thamChiếuLỗi] = bắtChạyPhươngThức[trịSố] + giáTrịNgắnKiểu();
                        bắtVịTrí[thamChiếuLỗi] = bắtChạyPhươngThức[trịSố] + giáTrịNgắnKiểu(); int giáTrịĐãMãHóa = đọcChỉSốHằng(); bắtLớp[thamChiếuLỗi] = giáTrịĐãMãHóa == 0 ? 0 : vănBảnTênLớp(giáTrịĐãMãHóa);
                    }
                    bỏBướcThuộcTính();
                    if (đọcVịTrí != chạy + độDài) giáTrịSựThấtBại("Code attribute size mismatch");
                } else bỏBướcCácByte(độDài);
            }
            if ((truyCậpPhươngThức[trịSố] & 0x400) != 0) continue;
            if (bắtChạyPhươngThức[trịSố] == 0) giáTrịSựThấtBại("missing Code attribute");
            int mụcÔ = bắtChạyPhươngThức[trịSố];
            while (mụcÔ < kếtThúcPhươngThức[trịSố] && !lỗi) {
                int độDài = đọcĐộDài(mụcÔ, bắtChạyPhươngThức[trịSố], kếtThúcPhươngThức[trịSố]);
                if (độDài == 0) { giáTrịSựThấtBại("unsupported or truncated bytecode"); break; }
                giáTrịRanhGiới[mụcÔ] = trịSố + 1; mụcÔ += độDài;
            }
            mụcÔ = bắtChạyPhươngThức[trịSố];
            while (mụcÔ < kếtThúcPhươngThức[trịSố] && !lỗi) {
                int giáTrị = Tệp[mụcÔ];
                if (giáTrị >= 153 && giáTrị <= 167 || giáTrị == 198 || giáTrị == 199) kiểmTraGiáTrịĐích(mụcÔ + (short)(Tệp[mụcÔ + 1] << 8 | Tệp[mụcÔ + 2]), trịSố);
                if (giáTrị == 200) kiểmTraGiáTrịĐích(mụcÔ + sốNguyênVịTrí(mụcÔ + 1), trịSố);
                if (giáTrị == 170 || giáTrị == 171) {
                    int đọcConTrỏVănBản = mụcÔ + 1; while ((đọcConTrỏVănBản - bắtChạyPhươngThức[trịSố]) % 4 != 0) đọcConTrỏVănBản++;
                    kiểmTraGiáTrịĐích(mụcÔ + sốNguyênVịTrí(đọcConTrỏVănBản), trịSố);
                    int sốLượngMục = giáTrị == 170 ? sốNguyênVịTrí(đọcConTrỏVănBản + 8) - sốNguyênVịTrí(đọcConTrỏVănBản + 4) + 1 : sốNguyênVịTrí(đọcConTrỏVănBản + 4);
                    đọcConTrỏVănBản += giáTrị == 170 ? 12 : 8;
                    for (int vịTríPhíaTrong = 0; vịTríPhíaTrong < sốLượngMục; vịTríPhíaTrong++) kiểmTraGiáTrịĐích(mụcÔ + sốNguyênVịTrí(đọcConTrỏVănBản + vịTríPhíaTrong * (giáTrị == 170 ? 4 : 8) + (giáTrị == 170 ? 0 : 4)), trịSố);
                }
                mụcÔ += đọcĐộDài(mụcÔ, bắtChạyPhươngThức[trịSố], kếtThúcPhươngThức[trịSố]);
            }
            for (int vịTríPhíaTrong = 0; vịTríPhíaTrong < bắtSốLượng; vịTríPhíaTrong++) if (bắtPhươngThức[vịTríPhíaTrong] == trịSố) {
                kiểmTraGiáTrịĐích(bắtBắtChạy[vịTríPhíaTrong], trịSố); kiểmTraGiáTrịĐích(bắtVịTrí[vịTríPhíaTrong], trịSố);
                if (bắtKếtThúc[vịTríPhíaTrong] != kếtThúcPhươngThức[trịSố]) kiểmTraGiáTrịĐích(bắtKếtThúc[vịTríPhíaTrong], trịSố);
                if (bắtBắtChạy[vịTríPhíaTrong] >= bắtKếtThúc[vịTríPhíaTrong]) giáTrịSựThấtBại("invalid exception range");
            }
        }
        if (!lỗi) bỏBướcThuộcTính();
        if (đọcVịTrí != cỡ) giáTrịSựThấtBại("extra class file data");
    }
    static int cấpPhátLưuTrữ(int giáTrịLoại, int độDài) { return bộNhớMới(giáTrịLoại, độDài); }
    static boolean giáTrịĐốiTượng(int thamChiếu, int giáTrịLoại) {
        if (!làĐốiTượngHợpLệ(thamChiếu)) return false;
        if (giáTrịVùngNhớĐộng[thamChiếu] != giáTrịLoại) { giáTrịSựThấtBại("object type mismatch"); return false; }
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
        if (kiểuTrảVề == 2) bảoVệGiáTrị(giáTrịNgănXếpToánHạng[mụcÔ]);
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
        if (chỉSốKhung % 32 == 31) { giáTrịSựThấtBại("call stack limit (32)"); return; }
        int phầnMụcKếTiếp = chỉSốKhung + 1;
        for (int trịSố = 0; trịSố < 128; trịSố++) kiểuCụcBộ[phầnMụcKếTiếp * 128 + trịSố] = 0;
        for (int trịSố = sốLượngĐốiSốPhươngThức[Hàm] - 1; trịSố >= 0; trịSố--) {
            giáTrịCụcBộ[phầnMụcKếTiếp * 128 + trịSố] = trừCácGiáTrị(kiểuĐốiSốPhươngThức[Hàm * 16 + trịSố]); kiểuCụcBộ[phầnMụcKếTiếp * 128 + trịSố] = kiểuĐốiSốPhươngThức[Hàm * 16 + trịSố];
        }
        if (lỗi) return;
        chỉSốKhung = phầnMụcKếTiếp; khởiTạoKhung[chỉSốKhung] = 0; phươngThứcKhung[chỉSốKhung] = Hàm; vịTríKhung[chỉSốKhung] = bắtChạyPhươngThức[Hàm]; ngănXếpKhung[chỉSốKhung] = 0;
    }
    static void kếtQuảTrảVề(int giáTrịKiểu) {
        if (giáTrịKiểu != trảVềPhươngThức[phươngThứcKhung[chỉSốKhung]]) { giáTrịSựThấtBại("return type mismatch"); return; }
        int giáTrị = giáTrịKiểu == 0 ? 0 : trừCácGiáTrị(giáTrịKiểu);
        if (khởiTạoKhung[chỉSốKhung] != 0) trạngTháiĐịnhNghĩaLớp[khởiTạoKhung[chỉSốKhung] - 1] = 2;
        if (khóaKhung[chỉSốKhung] != 0) { giảiPhóngKhóa(khóaKhung[chỉSốKhung]); khóaKhung[chỉSốKhung] = 0; }
        chỉSốKhung--; if (chỉSốKhung >= luồngChạyHiệnTại * 32 && giáTrịKiểu != 0) đặtGiáTrị(giáTrị, giáTrịKiểu);
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
                if (giáTrị < 1) { giáTrịSựThấtBại("invalid file stream path"); return; }
                tênTệpLuồng[mụcÔ] = giáTrị;
            }
            tênTệpLuồng[độDài] = 0;
            int mụcBộMôTả = NgườiDùng.mởBộMôTảTệp(tênTệpLuồng, ĐầuRa ? (giáTrịSựTiếpDiễn ? 1089 : 577) : 0);
            if (mụcBộMôTả < 0) { giáTrịSựThấtBại("FileNotFoundException: file open failed"); return; }
            giáTrịVùngNhớĐộng[giáTrịLuồng + 2] = mụcBộMôTả; giáTrịVùngNhớĐộng[giáTrịLuồng + 3] = 1;
            return;
        }
        if (lệnh != 182) { giáTrịSựThấtBại("invalid file stream invocation"); return; }
        if ((ĐầuRa && vănBảnTừ(tên, "write") || !ĐầuRa && vănBảnTừ(tên, "read"))
            && (vănBảnTừ(giáTrịĐịnhDạng, ĐầuRa ? "([B)V" : "([B)I") || vănBảnTừ(giáTrịĐịnhDạng, ĐầuRa ? "([BII)V" : "([BII)I"))) {
            boolean giáTrịCắtXén = vănBảnTừ(giáTrịĐịnhDạng, ĐầuRa ? "([BII)V" : "([BII)I");
            int sốLượngMục = giáTrịCắtXén ? trừCácGiáTrị(1) : 0, điểmĐangBắtChạy = giáTrịCắtXén ? trừCácGiáTrị(1) : 0, mảngDữLiệu = trừCácGiáTrị(2), thamChiếuĐốiTượng = trừCácGiáTrị(2);
            if (!giáTrịĐốiTượng(mảngDữLiệu, 20) || !giáTrịĐốiTượng(thamChiếuĐốiTượng, giáTrịLoại)) return;
            if (!giáTrịCắtXén) sốLượngMục = giáTrịVùngNhớĐộng[mảngDữLiệu + 1];
            if (điểmĐangBắtChạy < 0 || sốLượngMục < 0 || điểmĐangBắtChạy > giáTrịVùngNhớĐộng[mảngDữLiệu + 1] - sốLượngMục) { némNgoạiLệ(6, "file buffer bounds"); return; }
            if (giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 3] == 0 || giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2] < 0) { giáTrịSựThấtBại("IOException: stream closed"); return; }
            int sốLượngĐãHoànTất = 0;
            while (sốLượngĐãHoànTất < sốLượngMục && !lỗi) {
                int giáTrịĐãTrảVề = ĐầuRa ? NgườiDùng.ghiByteTệpMột(giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2], giáTrịVùngNhớĐộng[mảngDữLiệu + 2 + điểmĐangBắtChạy + sốLượngĐãHoànTất]) : NgườiDùng.đọcByteTệpMột(giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2]);
                if (giáTrịĐãTrảVề < 0) { giáTrịSựThấtBại(ĐầuRa ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!ĐầuRa && giáTrịĐãTrảVề == 256) break;
                if (!ĐầuRa) giáTrịVùngNhớĐộng[mảngDữLiệu + 2 + điểmĐangBắtChạy + sốLượngĐãHoànTất] = (byte)giáTrịĐãTrảVề;
                sốLượngĐãHoànTất++;
            }
            if (!ĐầuRa) đặtGiáTrị(sốLượngMục != 0 && sốLượngĐãHoànTất == 0 ? -1 : sốLượngĐãHoànTất, 1);
            return;
        }
        if (ĐầuRa && vănBảnTừ(tên, "flush") && vănBảnTừ(giáTrịĐịnhDạng, "()V")) { int thamChiếuĐốiTượng = trừCácGiáTrị(2); if (giáTrịĐốiTượng(thamChiếuĐốiTượng, giáTrịLoại) && giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2] < 0) giáTrịSựThấtBại("IOException: stream closed"); return; }
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
            if (kếtQuả < -1) giáTrịSựThấtBại("IOException: read failed"); else đặtGiáTrị(kếtQuả == 256 ? -1 : kếtQuả, 1);
        } else if (NgườiDùng.ghiByteTệpMột(mụcBộMôTả, giáTrị) != 1) giáTrịSựThấtBại("IOException: write failed");
    }
    static void gọiPhươngThức(int sốHiệu, int lệnh) {
        if (sốHiệu <= 0 || sốHiệu >= thẻHằng.length || (thẻHằng[sốHiệu] != 10 && thẻHằng[sốHiệu] != 11)) { giáTrịSựThấtBại("invalid method reference"); return; }
        int giáTrịChủSởHữu = vănBảnTênLớp(giáTrịĐầuTiênHằng[sốHiệu]), tên = tênThamChiếu(giáTrịThứHaiHằng[sốHiệu]), giáTrịĐịnhDạng = kiểuThamChiếu(giáTrịThứHaiHằng[sốHiệu]);
        if (lỗi) return;
        if (gọiThựcHiệnMặcĐịnh(giáTrịChủSởHữu, tên, giáTrịĐịnhDạng, lệnh)) return;
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
        int địnhNghĩaLớp = tìmĐịnhNghĩaLớp(giáTrịChủSởHữu); if (địnhNghĩaLớp < 0 || lỗi) return;
        int chỉSốTệp = tìmPhươngThức(địnhNghĩaLớp, tên, giáTrịĐịnhDạng);
        if (chỉSốTệp < 0) {
            for (int mãKýTự = địnhNghĩaLớp, sốLượngMục = 0; mãKýTự >= 0 && sốLượngMục < 16; sốLượngMục++, mãKýTự = lớpCha(mãKýTự))
                if (vănBảnTừ(chaĐịnhNghĩaLớp[mãKýTự], "java/lang/Thread")) { gọiThựcHiệnLuồngChạy(tên, giáTrịĐịnhDạng, lệnh); return; }
            giáTrịSựThấtBại("NoSuchMethodError"); return;
        }
        if (((truyCậpPhươngThức[chỉSốTệp] & 8) != 0) != (lệnh == 184)) { giáTrịSựThấtBại("method static/instance mismatch"); return; }
        if (lệnh == 184) { if (!khởiTạo(chủSởHữuPhươngThức[chỉSốTệp], chỉLệnhKhung[chỉSốKhung])) return; }
        else {
            int đọcConTrỏVănBản = ngănXếpKhung[chỉSốKhung] - sốLượngĐốiSốPhươngThức[chỉSốTệp];
            if (đọcConTrỏVănBản < 0 || kiểuNgănXếpToánHạng[chỉSốKhung * 128 + đọcConTrỏVănBản] != 2) { giáTrịSựThấtBại("invalid method receiver"); return; }
            int thamChiếuĐốiTượng = giáTrịNgănXếpToánHạng[chỉSốKhung * 128 + đọcConTrỏVănBản];
            if (!làĐốiTượngHợpLệ(thamChiếuĐốiTượng)) return;
            if (giáTrịVùngNhớĐộng[thamChiếuĐốiTượng] < 32 || !lớpChứa(giáTrịVùngNhớĐộng[thamChiếuĐốiTượng] - 32, giáTrịChủSởHữu)) { giáTrịSựThấtBại("method receiver type mismatch"); return; }
            if (lệnh != 183) chỉSốTệp = tìmPhươngThức(giáTrịVùngNhớĐộng[thamChiếuĐốiTượng] - 32, tên, giáTrịĐịnhDạng);
        }
        if (chỉSốTệp < 0 || (truyCậpPhươngThức[chỉSốTệp] & 0x400) != 0) { giáTrịSựThấtBại("AbstractMethodError"); return; }
        int thamChiếuKhóa = 0;
        if ((truyCậpPhươngThức[chỉSốTệp] & 32) != 0) {
            if (lệnh == 184) { int mãKýTự = chủSởHữuPhươngThức[chỉSốTệp]; if (khóaLớp[mãKýTự] == 0) khóaLớp[mãKýTự] = cấpPhátLưuTrữ(8, 0); thamChiếuKhóa = khóaLớp[mãKýTự]; }
            else thamChiếuKhóa = giáTrịNgănXếpToánHạng[chỉSốKhung * 128 + ngănXếpKhung[chỉSốKhung] - sốLượngĐốiSốPhươngThức[chỉSốTệp]];
            if (!thuNhậnKhóa(thamChiếuKhóa)) { if (!lỗi) vịTríKhung[chỉSốKhung] = chỉLệnhKhung[chỉSốKhung]; return; }
        }
        gọiThựcHiện(chỉSốTệp); if (!lỗi) khóaKhung[chỉSốKhung] = thamChiếuKhóa;
    }
    static boolean cóThểMảngCất(int thamChiếuMảng, int giáTrịDữLiệu) {
        if (giáTrịDữLiệu == 0 || phầnTửMảng[thamChiếuMảng] == 0) return true;
        boolean làĐãThànhCông = phầnTửMảng[thamChiếuMảng] == -1 ? (giáTrịDữLiệu > 0 && giáTrịDữLiệu < vịTríKếtThúcVùngNhớĐộng && giáTrịVùngNhớĐộng[giáTrịDữLiệu] == 1) : đốiTượngViệcSoKhớp(giáTrịDữLiệu, phầnTửMảng[thamChiếuMảng]);
        if (!làĐãThànhCông && !lỗi) némNgoạiLệ(17, "array element type mismatch");
        return làĐãThànhCông;
    }
    static int ôMảng(int thamChiếu, int giáTrịChỉSốDưới, int giáTrịKiểu) {
        if (!giáTrịĐốiTượng(thamChiếu, giáTrịKiểu)) return 0;
        if (giáTrịChỉSốDưới < 0 || giáTrịChỉSốDưới >= giáTrịVùngNhớĐộng[thamChiếu + 1]) { giáTrịSựThấtBại("ArrayIndexOutOfBoundsException"); return 0; }
        return thamChiếu + 2 + giáTrịChỉSốDưới;
    }
    static void thựcThiLệnh() {
        int dữLiệuSốDư = 500000, giáTrịĐoạn = 100;
        while (true) {
            if (lỗi) { if (đốiTượngĐãNém != 0) ngoạiLệThẻXửLý(); if (lỗi || chỉSốKhung < luồngChạyHiệnTại * 32) break; }
            if (chỉSốKhung < luồngChạyHiệnTại * 32 || đổiYêuCầu || --giáTrịĐoạn == 0) { if (!luồngChạyChuyển()) break; giáTrịĐoạn = 100; }
            if (chỉSốKhung == 0 && trạngTháiĐịnhNghĩaLớp[địnhNghĩaLớpMục] != 2 && !khởiTạo(địnhNghĩaLớpMục, vịTríKhung[chỉSốKhung])) continue;
            if (chỉSốKhung == luồngChạyHiệnTại * 32 && luồngChạyHiệnTại != 0 && (truyCậpPhươngThức[phươngThứcKhung[chỉSốKhung]] & 32) != 0 && khóaKhung[chỉSốKhung] == 0) {
                int thamChiếuĐốiTượng = đốiĐíchLuồngChạy[luồngChạyHiệnTại]; if (!thuNhậnKhóa(thamChiếuĐốiTượng)) { if (lỗi) break; continue; } khóaKhung[chỉSốKhung] = thamChiếuĐốiTượng;
            }
            sốLượngTạm = 0;
            if (--dữLiệuSốDư == 0) { giáTrịSựThấtBại("instruction limit (500000)"); break; }
            int chạy = vịTríKhung[chỉSốKhung]; chỉLệnhKhung[chỉSốKhung] = chạy; int giáTrị = đọcByteMãThaoTác();
            if (lỗi) break;
            if (giáTrị == 0) continue;
            if (giáTrị == 1) { đặtGiáTrị(0, 2); continue; }
            if (giáTrị >= 2 && giáTrị <= 8) { đặtGiáTrị(giáTrị - 3, 1); continue; }
            if (giáTrị == 16) { đặtGiáTrị((byte)đọcByteMãThaoTác(), 1); continue; }
            if (giáTrị == 17) { đặtGiáTrị((short)đọcNgắnKiểuMãThaoTác(), 1); continue; }
            if (giáTrị == 18 || giáTrị == 19) {
                int trịSố = chủSởHữuPhươngThức[phươngThứcKhung[chỉSốKhung]] * 512 + (giáTrị == 18 ? đọcByteMãThaoTác() : đọcNgắnKiểuMãThaoTác());
                if (trịSố <= 0 || trịSố >= thẻHằng.length) giáTrịSựThấtBại("invalid ldc constant");
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
            if (giáTrị == 46 || giáTrị >= 50 && giáTrị <= 53) {
                int vịTríMục = trừCácGiáTrị(1), thamChiếuĐốiTượng = trừCácGiáTrị(2), mãLoạiMục = giáTrị == 46 ? 2 : giáTrị == 50 ? 3 : giáTrị == 51 ? 20 : giáTrị == 52 ? 22 : 23;
                if (giáTrị == 51 && thamChiếuĐốiTượng > 0 && thamChiếuĐốiTượng < vịTríKếtThúcVùngNhớĐộng && giáTrịVùngNhớĐộng[thamChiếuĐốiTượng] == 21) mãLoạiMục = 21;
                int đọcConTrỏVănBản = ôMảng(thamChiếuĐốiTượng, vịTríMục, mãLoạiMục); if (!lỗi) đặtGiáTrị(giáTrịVùngNhớĐộng[đọcConTrỏVănBản], giáTrị == 50 ? 2 : 1); continue;
            }
            if (giáTrị == 79 || giáTrị >= 83 && giáTrị <= 86) {
                int thamChiếuMục = trừCácGiáTrị(giáTrị == 83 ? 2 : 1), vịTríMục = trừCácGiáTrị(1), thamChiếuĐốiTượng = trừCácGiáTrị(2), mãLoạiMục = giáTrị == 79 ? 2 : giáTrị == 83 ? 3 : giáTrị == 84 ? 20 : giáTrị == 85 ? 22 : 23;
                if (giáTrị == 84 && thamChiếuĐốiTượng > 0 && thamChiếuĐốiTượng < vịTríKếtThúcVùngNhớĐộng && giáTrịVùngNhớĐộng[thamChiếuĐốiTượng] == 21) mãLoạiMục = 21;
                int đọcConTrỏVănBản = ôMảng(thamChiếuĐốiTượng, vịTríMục, mãLoạiMục);
                if (!lỗi && mãLoạiMục == 3 && !cóThểMảngCất(thamChiếuĐốiTượng, thamChiếuMục)) continue;
                if (!lỗi) giáTrịVùngNhớĐộng[đọcConTrỏVănBản] = mãLoạiMục == 20 ? (byte)thamChiếuMục : mãLoạiMục == 21 ? thamChiếuMục & 1 : mãLoạiMục == 22 ? (char)thamChiếuMục : mãLoạiMục == 23 ? (short)thamChiếuMục : thamChiếuMục;
                continue;
            }
            if (giáTrị >= 87 && giáTrị <= 95) { chỉLệnhNgănXếp(giáTrị); continue; }
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
            if (giáTrị >= 178 && giáTrị <= 181) { gọiThựcHiệnTrường(đọcHằngMãThaoTác(), giáTrị, chạy); continue; }
            if (giáTrị >= 182 && giáTrị <= 185) {
                int giáTrịĐãMãHóa = đọcHằngMãThaoTác();
                if (giáTrị == 185) { int sốLượngTổngCộng = đọcByteMãThaoTác(); if (sốLượngTổngCộng == 0 || đọcByteMãThaoTác() != 0) { giáTrịSựThấtBại("invalid invokeinterface operands"); continue; } }
                gọiPhươngThức(giáTrịĐãMãHóa, giáTrị); continue;
            }
            if (giáTrị == 187) { đốiTượngMới(vănBảnTênLớp(đọcHằngMãThaoTác()), chạy); continue; }
            if (giáTrị == 188 || giáTrị == 189) {
                int mãLoạiMục = 3, thànhPhần = 0;
                if (giáTrị == 188) { int dữLiệuTạm = đọcByteMãThaoTác(); mãLoạiMục = dữLiệuTạm == 10 ? 2 : dữLiệuTạm == 8 ? 20 : dữLiệuTạm == 4 ? 21 : dữLiệuTạm == 5 ? 22 : dữLiệuTạm == 9 ? 23 : 0; }
                else thànhPhần = vănBảnTênLớp(đọcHằngMãThaoTác());
                if (mãLoạiMục == 0) { giáTrịSựThấtBại("unsupported primitive array type"); continue; }
                int độDàiHợpLệ = trừCácGiáTrị(1), thamChiếuĐốiTượng = cấpPhátLưuTrữ(mãLoạiMục, độDàiHợpLệ); if (!lỗi) phầnTửMảng[thamChiếuĐốiTượng] = thànhPhần; đặtGiáTrị(thamChiếuĐốiTượng, 2); continue;
            }
            if (giáTrị == 190) {
                int thamChiếuĐốiTượng = trừCácGiáTrị(2);
                if (làĐốiTượngHợpLệ(thamChiếuĐốiTượng)) { int vịTríPhépSoSánh = giáTrịVùngNhớĐộng[thamChiếuĐốiTượng]; if (vịTríPhépSoSánh != 2 && vịTríPhépSoSánh != 3 && (vịTríPhépSoSánh < 20 || vịTríPhépSoSánh > 23)) giáTrịSựThấtBại("not an array"); else đặtGiáTrị(giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 1], 1); }
                continue;
            }
            if (giáTrị == 191) {
                int thamChiếuĐốiTượng = trừCácGiáTrị(2); if (làĐốiTượngHợpLệ(thamChiếuĐốiTượng)) { if (giáTrịVùngNhớĐộng[thamChiếuĐốiTượng] != 9) giáTrịSựThấtBại("athrow requires supported Throwable"); else { đốiTượngĐãNém = thamChiếuĐốiTượng; lỗi = true; } }
                continue;
            }
            if (giáTrị == 192 || giáTrị == 193) {
                int hằngTên = vănBảnTênLớp(đọcHằngMãThaoTác()), thamChiếuĐốiTượng = trừCácGiáTrị(2); boolean cóKhớp = đốiTượngViệcSoKhớp(thamChiếuĐốiTượng, hằngTên);
                if (giáTrị == 193) đặtGiáTrị(thamChiếuĐốiTượng != 0 && cóKhớp ? 1 : 0, 1);
                else { if (!cóKhớp && !lỗi) giáTrịSựThấtBại("ClassCastException"); đặtGiáTrị(thamChiếuĐốiTượng, 2); }
                continue;
            }
            if (giáTrị == 170 || giáTrị == 171) {
                int đọcConTrỏVănBản = chạy + 1, chỉSốTệp = phươngThứcKhung[chỉSốKhung], thamChiếuPhím = trừCácGiáTrị(1);
                while ((đọcConTrỏVănBản - bắtChạyPhươngThức[chỉSốTệp]) % 4 != 0) đọcConTrỏVănBản++;
                int địaChỉĐốiĐích = sốNguyênVịTrí(đọcConTrỏVănBản);
                if (giáTrị == 170) { int giáTrịThấp = sốNguyênVịTrí(đọcConTrỏVănBản + 4), giáTrịCaoTrên = sốNguyênVịTrí(đọcConTrỏVănBản + 8); if (thamChiếuPhím >= giáTrịThấp && thamChiếuPhím <= giáTrịCaoTrên) địaChỉĐốiĐích = sốNguyênVịTrí(đọcConTrỏVănBản + 12 + (thamChiếuPhím - giáTrịThấp) * 4); }
                else { int sốLượngTổngCộng = sốNguyênVịTrí(đọcConTrỏVănBản + 4); for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < sốLượngTổngCộng; chỉSốVòngLặp++) if (sốNguyênVịTrí(đọcConTrỏVănBản + 8 + chỉSốVòngLặp * 8) == thamChiếuPhím) địaChỉĐốiĐích = sốNguyênVịTrí(đọcConTrỏVănBản + 12 + chỉSốVòngLặp * 8); }
                giáTrịDiChuyển(chạy + địaChỉĐốiĐích); continue;
            }
            if (giáTrị == 200) { giáTrịDiChuyển(chạy + sốNguyênVịTrí(chạy + 1)); continue; }
            if (giáTrị == 194 || giáTrị == 195) {
                int thamChiếuĐốiTượng = trừCácGiáTrị(2);
                if (giáTrị == 195) giảiPhóngKhóa(thamChiếuĐốiTượng);
                else if (!thuNhậnKhóa(thamChiếuĐốiTượng) && !lỗi) { đặtGiáTrị(thamChiếuĐốiTượng, 2); vịTríKhung[chỉSốKhung] = chạy; }
                continue;
            }
            if (giáTrị == 196) {
                int mãLệnh = đọcByteMãThaoTác(), vịTríMục = đọcNgắnKiểuMãThaoTác();
                if (mãLệnh == 21 || mãLệnh == 25) đọcCụcBộ(vịTríMục, mãLệnh == 21 ? 1 : 2);
                else if (mãLệnh == 54 || mãLệnh == 58) ghiCụcBộ(vịTríMục, mãLệnh == 54 ? 1 : 2);
                else if (mãLệnh == 132) { int giáTrịĐộChênh = (short)đọcNgắnKiểuMãThaoTác(); đọcCụcBộ(vịTríMục, 1); đặtGiáTrị(trừCácGiáTrị(1) + giáTrịĐộChênh, 1); ghiCụcBộ(vịTríMục, 1); }
                else giáTrịSựThấtBại("unsupported wide opcode");
                continue;
            }
            giáTrịSựThấtBại("unsupported bytecode");
        }
    }
    static int tìmĐịnhNghĩaLớp(int tên) {
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < sốLượngĐịnhNghĩaLớp; chỉSốVòngLặp++) if (tênĐịnhNghĩaLớp[chỉSốVòngLặp] != 0 && từViệcSoKhớp(tênĐịnhNghĩaLớp[chỉSốVòngLặp], tên)) return chỉSốVòngLặp;
        return nạpĐịnhNghĩaLớp(vănBảnHằng(tên));
    }
    static int nạpĐịnhNghĩaLớp(int chuỗiTên) {
        if (!giáTrịĐốiTượng(chuỗiTên, 1)) return -1;
        int độDài = giáTrịVùngNhớĐộng[chuỗiTên + 1];
        if (độDài < 1 || độDài > 505 || sốLượngĐịnhNghĩaLớp == 16) { giáTrịSựThấtBại("class name/count limit"); return -1; }
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < độDài; chỉSốVòngLặp++) { int mãKýTự = giáTrịVùngNhớĐộng[chuỗiTên + 2 + chỉSốVòngLặp]; vănBảnTênTệp[chỉSốVòngLặp] = mãKýTự == '/' ? '.' : mãKýTự; }
        vănBảnTênTệp[độDài] = '.'; vănBảnTênTệp[độDài + 1] = 'c'; vănBảnTênTệp[độDài + 2] = 'l'; vănBảnTênTệp[độDài + 3] = 'a'; vănBảnTênTệp[độDài + 4] = 's'; vănBảnTênTệp[độDài + 5] = 's'; vănBảnTênTệp[độDài + 6] = 0;
        int cỡ = NgườiDùng.đọcTệp(vănBảnTênTệp, tệpTạm);
        if (cỡ < 0) { giáTrịSựThấtBại("ClassNotFoundException"); return -1; }
        int địnhNghĩaLớp = sốLượngĐịnhNghĩaLớp++; cỡĐịnhNghĩaLớp[địnhNghĩaLớp] = cỡ;
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < cỡ; chỉSốVòngLặp++) Tệp[địnhNghĩaLớp * 16384 + chỉSốVòngLặp] = tệpTạm[chỉSốVòngLặp];
        đọcLớp(địnhNghĩaLớp); if (lỗi) return -1;
        int dữLiệuThựcTế = vănBảnHằng(tênĐịnhNghĩaLớp[địnhNghĩaLớp]);
        if (!bằngCácVănBản(dữLiệuThựcTế, chuỗiTên, true)) { giáTrịSựThấtBại("class name does not match file"); return -1; }
        int giáTrịCha = chaĐịnhNghĩaLớp[địnhNghĩaLớp];
        if (giáTrịCha != 0 && !vănBảnTừ(giáTrịCha, "java/lang/Object") && !vănBảnTừ(giáTrịCha, "java/lang/Thread")) {
            // Không nạp lại lớp đã đăng ký, nhưng từ chối tường minh chu trình kế thừa.
            int giáTrịĐỉnh = tìmĐịnhNghĩaLớp(giáTrịCha);
            if (lỗi || giáTrịĐỉnh < 0) return -1;
            int đọcConTrỏVănBản = giáTrịĐỉnh, sốLượngGiaiĐoạn = 0;
            while (đọcConTrỏVănBản >= 0 && sốLượngGiaiĐoạn++ < 16) {
                if (đọcConTrỏVănBản == địnhNghĩaLớp) { giáTrịSựThấtBại("cyclic inheritance"); return -1; }
                đọcConTrỏVănBản = lớpCha(đọcConTrỏVănBản);
            }
            int bắtChạyĐộDời = sốLượngÔLớp[giáTrịĐỉnh];
            for (int chỉSốTệp = 0; chỉSốTệp < sốLượngÔ; chỉSốTệp++) if (chủSởHữuÔ[chỉSốTệp] == địnhNghĩaLớp && (cácQuyềnÔ[chỉSốTệp] & 8) == 0) vịTríÔ[chỉSốTệp] += bắtChạyĐộDời;
            sốLượngÔLớp[địnhNghĩaLớp] += bắtChạyĐộDời;
        }
        return địnhNghĩaLớp;
    }
    static int lớpCha(int địnhNghĩaLớp) {
        int tên = chaĐịnhNghĩaLớp[địnhNghĩaLớp];
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < sốLượngĐịnhNghĩaLớp; chỉSốVòngLặp++) if (tên != 0 && tênĐịnhNghĩaLớp[chỉSốVòngLặp] != 0 && từViệcSoKhớp(tênĐịnhNghĩaLớp[chỉSốVòngLặp], tên)) return chỉSốVòngLặp;
        return -1;
    }
    static int tìmPhươngThức(int địnhNghĩaLớp, int tên, int giáTrịĐịnhDạng) {
        for (int giáTrịĐộSâu = 0; địnhNghĩaLớp >= 0 && giáTrịĐộSâu < 16; giáTrịĐộSâu++, địnhNghĩaLớp = lớpCha(địnhNghĩaLớp)) {
            for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < sốLượngPhươngThức; chỉSốVòngLặp++) if (chủSởHữuPhươngThức[chỉSốVòngLặp] == địnhNghĩaLớp && từViệcSoKhớp(vănBảnTênPhươngThức[chỉSốVòngLặp], tên) && từViệcSoKhớp(kiểuPhươngThức[chỉSốVòngLặp], giáTrịĐịnhDạng)) return chỉSốVòngLặp;
        }
        return -1;
    }
    static int phươngThứcTên(int địnhNghĩaLớp, String tên, String giáTrịĐịnhDạng) {
        for (int giáTrịĐộSâu = 0; địnhNghĩaLớp >= 0 && giáTrịĐộSâu < 16; giáTrịĐộSâu++, địnhNghĩaLớp = lớpCha(địnhNghĩaLớp))
            for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < sốLượngPhươngThức; chỉSốVòngLặp++) if (chủSởHữuPhươngThức[chỉSốVòngLặp] == địnhNghĩaLớp && vănBảnTừ(vănBảnTênPhươngThức[chỉSốVòngLặp], tên) && vănBảnTừ(kiểuPhươngThức[chỉSốVòngLặp], giáTrịĐịnhDạng)) return chỉSốVòngLặp;
        return -1;
    }
    static int loạiKiểu(int tên) { return Tệp[giáTrịĐầuTiênHằng[tên]] == 'L' || Tệp[giáTrịĐầuTiênHằng[tên]] == '[' ? 2 : 1; }
    static boolean khởiTạo(int địnhNghĩaLớp, int bắtChạyLệnh) {
        if (địnhNghĩaLớp < 0 || lỗi) return false;
        if (trạngTháiĐịnhNghĩaLớp[địnhNghĩaLớp] == 3) { giáTrịSựThấtBại("NoClassDefFoundError: initialization failed"); return false; }
        if (trạngTháiĐịnhNghĩaLớp[địnhNghĩaLớp] == 1 && luồngChạyLớp[địnhNghĩaLớp] != luồngChạyHiệnTại) { vịTríKhung[chỉSốKhung] = bắtChạyLệnh; đổiYêuCầu = true; return false; }
        if (trạngTháiĐịnhNghĩaLớp[địnhNghĩaLớp] != 0) return true;
        int giáTrịĐỉnh = lớpCha(địnhNghĩaLớp);
        if (giáTrịĐỉnh >= 0 && !khởiTạo(giáTrịĐỉnh, bắtChạyLệnh)) return false;
        trạngTháiĐịnhNghĩaLớp[địnhNghĩaLớp] = 1; luồngChạyLớp[địnhNghĩaLớp] = luồngChạyHiệnTại;
        if (khởiTạoĐịnhNghĩaLớp[địnhNghĩaLớp] != 0) {
            vịTríKhung[chỉSốKhung] = bắtChạyLệnh;
            gọiThựcHiện(khởiTạoĐịnhNghĩaLớp[địnhNghĩaLớp] - 1); if (!lỗi) khởiTạoKhung[chỉSốKhung] = địnhNghĩaLớp + 1;
            return false;
        }
        trạngTháiĐịnhNghĩaLớp[địnhNghĩaLớp] = 2; return true;
    }
    static void gọiThựcHiệnTrường(int sốHiệu, int lệnh, int chạy) {
        if (!kiểmTraHằng(sốHiệu, 9)) return;
        int giáTrịChủSởHữu = vănBảnTênLớp(giáTrịĐầuTiênHằng[sốHiệu]), tên = tênThamChiếu(giáTrịThứHaiHằng[sốHiệu]), giáTrịĐịnhDạng = kiểuThamChiếu(giáTrịThứHaiHằng[sốHiệu]);
        if (vănBảnTừ(giáTrịChủSởHữu, "java/lang/System") && (vănBảnTừ(tên, "out") || vănBảnTừ(tên, "err")) && vănBảnTừ(giáTrịĐịnhDạng, "Ljava/io/PrintStream;") && lệnh == 178) { đặtGiáTrị(-1, 2); return; }
        int địnhNghĩaLớp = tìmĐịnhNghĩaLớp(giáTrịChủSởHữu); if (địnhNghĩaLớp < 0 || lỗi) return;
        int giáTrịĐãTìmThấy = -1;
        for (int đọcConTrỏVănBản = địnhNghĩaLớp, giáTrịĐộSâu = 0; đọcConTrỏVănBản >= 0 && giáTrịĐộSâu < 16 && giáTrịĐãTìmThấy < 0; giáTrịĐộSâu++, đọcConTrỏVănBản = lớpCha(đọcConTrỏVănBản))
            for (int chỉSốTệp = 0; chỉSốTệp < sốLượngÔ; chỉSốTệp++) if (chủSởHữuÔ[chỉSốTệp] == đọcConTrỏVănBản && từViệcSoKhớp(tênÔ[chỉSốTệp], tên) && từViệcSoKhớp(kiểuÔ[chỉSốTệp], giáTrịĐịnhDạng)) giáTrịĐãTìmThấy = chỉSốTệp;
        if (giáTrịĐãTìmThấy < 0) { giáTrịSựThấtBại("NoSuchFieldError"); return; }
        boolean giáTrịTĩnh = lệnh == 178 || lệnh == 179;
        if (giáTrịTĩnh != ((cácQuyềnÔ[giáTrịĐãTìmThấy] & 8) != 0)) { giáTrịSựThấtBại("field static/instance mismatch"); return; }
        if (giáTrịTĩnh && !khởiTạo(chủSởHữuÔ[giáTrịĐãTìmThấy], chạy)) return;
        int giáTrịKiểu = loạiKiểu(giáTrịĐịnhDạng), giáTrị = 0;
        if (lệnh == 179 || lệnh == 181) giáTrị = trừCácGiáTrị(giáTrịKiểu);
        if (giáTrịTĩnh) { if (lệnh == 178) đặtGiáTrị(dữLiệuÔ[giáTrịĐãTìmThấy], giáTrịKiểu); else if (!lỗi) dữLiệuÔ[giáTrịĐãTìmThấy] = giáTrị; return; }
        int thamChiếuĐốiTượng = trừCácGiáTrị(2);
        if (!làĐốiTượngHợpLệ(thamChiếuĐốiTượng)) return;
        if (giáTrịVùngNhớĐộng[thamChiếuĐốiTượng] < 32 || !lớpChứa(giáTrịVùngNhớĐộng[thamChiếuĐốiTượng] - 32, giáTrịChủSởHữu)) { giáTrịSựThấtBại("field receiver type mismatch"); return; }
        int ôĐãGiữNguyên = thamChiếuĐốiTượng + 2 + vịTríÔ[giáTrịĐãTìmThấy];
        if (lệnh == 180) đặtGiáTrị(giáTrịVùngNhớĐộng[ôĐãGiữNguyên], giáTrịKiểu);
        else if (!lỗi) { giáTrịVùngNhớĐộng[ôĐãGiữNguyên] = giáTrị; thamChiếuVùngNhớĐộng[ôĐãGiữNguyên] = giáTrịKiểu == 2 ? 1 : 0; }
    }
    static boolean lớpChứa(int địnhNghĩaLớp, int tên) {
        for (int độSâu = 0; địnhNghĩaLớp >= 0 && độSâu < 16; độSâu++, địnhNghĩaLớp = lớpCha(địnhNghĩaLớp)) {
            if (từViệcSoKhớp(tênĐịnhNghĩaLớp[địnhNghĩaLớp], tên) || (chaĐịnhNghĩaLớp[địnhNghĩaLớp] != 0 && từViệcSoKhớp(chaĐịnhNghĩaLớp[địnhNghĩaLớp], tên))) return true;
            for (int vịTríPhíaTrong = 0; vịTríPhíaTrong < sốLượngGiaoDiệnLớp[địnhNghĩaLớp]; vịTríPhíaTrong++) if (từViệcSoKhớp(giaoDiệnLớp[địnhNghĩaLớp * 16 + vịTríPhíaTrong], tên)) return true;
        }
        return false;
    }
    static boolean bằngCácVănBản(int dữLiệuĐầuTiên, int dữLiệuByte, boolean đườngDẫn) {
        if (dữLiệuĐầuTiên == dữLiệuByte) return true;
        if (dữLiệuĐầuTiên <= 0 || dữLiệuByte <= 0 || giáTrịVùngNhớĐộng[dữLiệuĐầuTiên] != 1 || giáTrịVùngNhớĐộng[dữLiệuByte] != 1 || giáTrịVùngNhớĐộng[dữLiệuĐầuTiên + 1] != giáTrịVùngNhớĐộng[dữLiệuByte + 1]) return false;
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < giáTrịVùngNhớĐộng[dữLiệuĐầuTiên + 1]; chỉSốVòngLặp++) {
            int tọaĐộX = giáTrịVùngNhớĐộng[dữLiệuĐầuTiên + 2 + chỉSốVòngLặp], tọaĐộY = giáTrịVùngNhớĐộng[dữLiệuByte + 2 + chỉSốVòngLặp];
            if (đườngDẫn) { if (tọaĐộX == '.') tọaĐộX = '/'; if (tọaĐộY == '.') tọaĐộY = '/'; }
            if (tọaĐộX != tọaĐộY) return false;
        }
        return true;
    }
    static boolean làĐốiTượngHợpLệ(int thamChiếuĐốiTượng) {
        if (thamChiếuĐốiTượng == 0) { giáTrịSựThấtBại("NullPointerException"); return false; }
        if (thamChiếuĐốiTượng < 1 || thamChiếuĐốiTượng >= vịTríKếtThúcVùngNhớĐộng || rộngVùngNhớĐộng[thamChiếuĐốiTượng] < 2 || giáTrịVùngNhớĐộng[thamChiếuĐốiTượng] == 0) { giáTrịSựThấtBại("invalid object reference"); return false; }
        return true;
    }
    static void bảoVệGiáTrị(int thamChiếuĐốiTượng) {
        if (thamChiếuĐốiTượng > 0 && thamChiếuĐốiTượng < vịTríKếtThúcVùngNhớĐộng && rộngVùngNhớĐộng[thamChiếuĐốiTượng] >= 2 && sốLượngTạm < thamChiếuTạm.length) thamChiếuTạm[sốLượngTạm++] = thamChiếuĐốiTượng;
    }
    static void hiệnGiáTrị(int thamChiếuĐốiTượng) {
        if (thamChiếuĐốiTượng > 0 && thamChiếuĐốiTượng < vịTríKếtThúcVùngNhớĐộng && rộngVùngNhớĐộng[thamChiếuĐốiTượng] >= 2 && giáTrịVùngNhớĐộng[thamChiếuĐốiTượng] != 0 && dấuVùngNhớĐộng[thamChiếuĐốiTượng] == 0) {
            dấuVùngNhớĐộng[thamChiếuĐốiTượng] = 1; chờHiểnThịCho[sốLượngHiểnThị++] = thamChiếuĐốiTượng;
        }
    }
    static void thuThậpRác() {
        sốLượngHiểnThị = 0; sốLượngTậpHợp++;
        for (int kiểmTraVịTrí = 1; kiểmTraVịTrí < vịTríKếtThúcVùngNhớĐộng; kiểmTraVịTrí += rộngVùngNhớĐộng[kiểmTraVịTrí]) dấuVùngNhớĐộng[kiểmTraVịTrí] = 0;
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < thamChiếuChuỗi.length; chỉSốVòngLặp++) hiệnGiáTrị(thamChiếuChuỗi[chỉSốVòngLặp]);
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < sốLượngÔ; chỉSốVòngLặp++) if ((cácQuyềnÔ[chỉSốVòngLặp] & 8) != 0 && loạiKiểu(kiểuÔ[chỉSốVòngLặp]) == 2) hiệnGiáTrị(dữLiệuÔ[chỉSốVòngLặp]);
        for (int dữLiệuTạm = 0; dữLiệuTạm < sốLượngLuồngChạy; dữLiệuTạm++) {
            hiệnGiáTrị(đốiTượngLuồngChạy[dữLiệuTạm]); hiệnGiáTrị(đốiĐíchLuồngChạy[dữLiệuTạm]);
            int vịTríĐỉnh = dữLiệuTạm == luồngChạyHiệnTại ? chỉSốKhung : khungLuồngChạy[dữLiệuTạm];
            for (int chỉSốTệp = dữLiệuTạm * 32; chỉSốTệp <= vịTríĐỉnh; chỉSốTệp++) {
                for (int vịTríPhíaTrong = 0; vịTríPhíaTrong < cácBiếnCụcBộPhươngThức[phươngThứcKhung[chỉSốTệp]]; vịTríPhíaTrong++) if (kiểuCụcBộ[chỉSốTệp * 128 + vịTríPhíaTrong] == 2) hiệnGiáTrị(giáTrịCụcBộ[chỉSốTệp * 128 + vịTríPhíaTrong]);
                for (int vịTríPhíaTrong = 0; vịTríPhíaTrong < ngănXếpKhung[chỉSốTệp]; vịTríPhíaTrong++) if (kiểuNgănXếpToánHạng[chỉSốTệp * 128 + vịTríPhíaTrong] == 2) hiệnGiáTrị(giáTrịNgănXếpToánHạng[chỉSốTệp * 128 + vịTríPhíaTrong]);
            }
        }
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < thamChiếuMànHình.length; chỉSốVòngLặp++) hiệnGiáTrị(thamChiếuMànHình[chỉSốVòngLặp]);
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < sốLượngVềSau; chỉSốVòngLặp++) hiệnGiáTrị(vềSauLậpLịch[chỉSốVòngLặp]);
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < sốNguyênCất.length; chỉSốVòngLặp++) hiệnGiáTrị(sốNguyênCất[chỉSốVòngLặp]);
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < sốLượngĐịnhNghĩaLớp; chỉSốVòngLặp++) hiệnGiáTrị(khóaLớp[chỉSốVòngLặp]);
        for (int kiểmTraVịTrí = 1; kiểmTraVịTrí < vịTríKếtThúcVùngNhớĐộng; kiểmTraVịTrí += rộngVùngNhớĐộng[kiểmTraVịTrí]) if (độSâuKhóa[kiểmTraVịTrí] > 0) hiệnGiáTrị(kiểmTraVịTrí);
        hiệnGiáTrị(đốiTượngĐãNém);
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < sốLượngTạm; chỉSốVòngLặp++) hiệnGiáTrị(thamChiếuTạm[chỉSốVòngLặp]);
        while (sốLượngHiểnThị > 0) {
            int thamChiếuĐốiTượng = chờHiểnThịCho[--sốLượngHiểnThị], mãLoạiMục = giáTrịVùngNhớĐộng[thamChiếuĐốiTượng];
            for (int chỉSốVòngLặp = thamChiếuĐốiTượng + 2; chỉSốVòngLặp < thamChiếuĐốiTượng + rộngVùngNhớĐộng[thamChiếuĐốiTượng]; chỉSốVòngLặp++) if (mãLoạiMục == 3 || mãLoạiMục == 4 || thamChiếuVùngNhớĐộng[chỉSốVòngLặp] != 0) hiệnGiáTrị(giáTrịVùngNhớĐộng[chỉSốVòngLặp]);
        }
        for (int kiểmTraVịTrí = 1; kiểmTraVịTrí < vịTríKếtThúcVùngNhớĐộng; kiểmTraVịTrí += rộngVùngNhớĐộng[kiểmTraVịTrí]) if (dấuVùngNhớĐộng[kiểmTraVịTrí] == 0) giáTrịVùngNhớĐộng[kiểmTraVịTrí] = 0;
        for (int kiểmTraVịTrí = 1; kiểmTraVịTrí < vịTríKếtThúcVùngNhớĐộng; kiểmTraVịTrí += rộngVùngNhớĐộng[kiểmTraVịTrí]) if (giáTrịVùngNhớĐộng[kiểmTraVịTrí] == 0) {
            while (kiểmTraVịTrí + rộngVùngNhớĐộng[kiểmTraVịTrí] < vịTríKếtThúcVùngNhớĐộng && giáTrịVùngNhớĐộng[kiểmTraVịTrí + rộngVùngNhớĐộng[kiểmTraVịTrí]] == 0) { int vịTríKếTiếp = kiểmTraVịTrí + rộngVùngNhớĐộng[kiểmTraVịTrí]; rộngVùngNhớĐộng[kiểmTraVịTrí] += rộngVùngNhớĐộng[vịTríKếTiếp]; rộngVùngNhớĐộng[vịTríKếTiếp] = 0; }
            if (kiểmTraVịTrí + rộngVùngNhớĐộng[kiểmTraVịTrí] == vịTríKếtThúcVùngNhớĐộng) { vịTríKếtThúcVùngNhớĐộng = kiểmTraVịTrí; break; }
        }
    }
    static int bộNhớMới(int giáTrịLoại, int độDài) {
        if (độDài < 0) { giáTrịSựThấtBại("NegativeArraySizeException"); return 0; }
        if (độDài > giáTrịVùngNhớĐộng.length - 3) { giáTrịSựThấtBại("object heap exhausted"); return 0; }
        int sốLượngBắtBuộc = độDài + 2, thamChiếuĐốiTượng = 0;
        if (sốLượngBắtBuộc <= giáTrịVùngNhớĐộng.length - vịTríKếtThúcVùngNhớĐộng) { thamChiếuĐốiTượng = vịTríKếtThúcVùngNhớĐộng; vịTríKếtThúcVùngNhớĐộng += sốLượngBắtBuộc; }
        else {
            thuThậpRác();
            for (int đọcConTrỏVănBản = 1; đọcConTrỏVănBản < vịTríKếtThúcVùngNhớĐộng; đọcConTrỏVănBản += rộngVùngNhớĐộng[đọcConTrỏVănBản]) if (giáTrịVùngNhớĐộng[đọcConTrỏVănBản] == 0 && rộngVùngNhớĐộng[đọcConTrỏVănBản] >= sốLượngBắtBuộc) { thamChiếuĐốiTượng = đọcConTrỏVănBản; break; }
            if (thamChiếuĐốiTượng != 0) {
                int độDàiCònLại = rộngVùngNhớĐộng[thamChiếuĐốiTượng] - sốLượngBắtBuộc;
                if (độDàiCònLại >= 2) { rộngVùngNhớĐộng[thamChiếuĐốiTượng + sốLượngBắtBuộc] = độDàiCònLại; giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + sốLượngBắtBuộc] = 0; }
                else sốLượngBắtBuộc += độDàiCònLại;
            } else if (sốLượngBắtBuộc <= giáTrịVùngNhớĐộng.length - vịTríKếtThúcVùngNhớĐộng) { thamChiếuĐốiTượng = vịTríKếtThúcVùngNhớĐộng; vịTríKếtThúcVùngNhớĐộng += sốLượngBắtBuộc; }
        }
        if (thamChiếuĐốiTượng == 0) { giáTrịSựThấtBại("object heap exhausted"); return 0; }
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < sốLượngBắtBuộc; chỉSốVòngLặp++) { giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + chỉSốVòngLặp] = 0; thamChiếuVùngNhớĐộng[thamChiếuĐốiTượng + chỉSốVòngLặp] = 0; rộngVùngNhớĐộng[thamChiếuĐốiTượng + chỉSốVòngLặp] = 0; }
        phầnTửMảng[thamChiếuĐốiTượng] = 0;
        rộngVùngNhớĐộng[thamChiếuĐốiTượng] = sốLượngBắtBuộc; giáTrịVùngNhớĐộng[thamChiếuĐốiTượng] = giáTrịLoại; giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 1] = độDài; bảoVệGiáTrị(thamChiếuĐốiTượng); return thamChiếuĐốiTượng;
    }
    static int lớpNgoạiLệ(String hằngTên) {
        if (CôngCụJava.vănBảnBằng(hằngTên, "java/lang/Throwable")) return 1;
        if (CôngCụJava.vănBảnBằng(hằngTên, "java/lang/Exception")) return 2;
        if (CôngCụJava.vănBảnBằng(hằngTên, "java/lang/RuntimeException")) return 3;
        if (CôngCụJava.vănBảnBằng(hằngTên, "java/lang/ArithmeticException")) return 4;
        if (CôngCụJava.vănBảnBằng(hằngTên, "java/lang/NullPointerException")) return 5;
        if (CôngCụJava.vănBảnBằng(hằngTên, "java/lang/IndexOutOfBoundsException")) return 6;
        if (CôngCụJava.vănBảnBằng(hằngTên, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (CôngCụJava.vănBảnBằng(hằngTên, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (CôngCụJava.vănBảnBằng(hằngTên, "java/lang/IllegalArgumentException")) return 9;
        if (CôngCụJava.vănBảnBằng(hằngTên, "java/lang/NumberFormatException")) return 10;
        if (CôngCụJava.vănBảnBằng(hằngTên, "java/io/IOException")) return 11;
        if (CôngCụJava.vănBảnBằng(hằngTên, "java/io/FileNotFoundException")) return 12;
        if (CôngCụJava.vănBảnBằng(hằngTên, "java/lang/IllegalStateException")) return 13;
        if (CôngCụJava.vănBảnBằng(hằngTên, "java/lang/ClassCastException")) return 14;
        if (CôngCụJava.vănBảnBằng(hằngTên, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int hằngNgoạiLệ(int tên) {
        for (int chỉSốVòngLặp = 1; chỉSốVòngLặp <= 41; chỉSốVòngLặp++) if (vănBảnTừ(tên, tênNgoạiLệ(chỉSốVòngLặp))) return chỉSốVòngLặp;
        return 0;
    }
    static String tênNgoạiLệ(int giáTrịCănCước) {
        if (giáTrịCănCước == 40) return "java/lang/InterruptedException";
        if (giáTrịCănCước == 41) return "tiếngViệt/tựThân/NgoạiLệĐãBịNgắtChờ";
        if (giáTrịCănCước == 39) return "java/net/SocketException";
        if (giáTrịCănCước == 20) return "tiếngViệt/tựThân/ngoạiLệ";
        if (giáTrịCănCước == 21) return "tiếngViệt/tựThân/NgoạiLệViệcThựcThi";
        if (giáTrịCănCước == 22) return "tiếngViệt/tựThân/NgoạiLệĐầuRaĐầuVào";
        if (giáTrịCănCước == 23) return "tiếngViệt/tựThân/NgoạiLệHếtGiờChờ";
        if (giáTrịCănCước == 24) return "tiếngViệt/tựThân/NgoạiLệTraCứuĐịaChỉ";
        if (giáTrịCănCước == 25) return "tiếngViệt/tựThân/NgoạiLệTệpThiếu";
        if (giáTrịCănCước == 26) return "tiếngViệt/tựThân/NgoạiLệTruyềnThông";
        if (giáTrịCănCước == 27) return "tiếngViệt/tựThân/NgoạiLệĐốiSốKhôngHợpLệ";
        if (giáTrịCănCước == 28) return "tiếngViệt/tựThân/SựThấtBạiĐịnhDạngSố";
        if (giáTrịCănCước == 29) return "tiếngViệt/tựThân/NgoạiLệCácCận";
        if (giáTrịCănCước == 30) return "tiếngViệt/tựThân/NgoạiLệCácCậnMảng";
        if (giáTrịCănCước == 31) return "tiếngViệt/tựThân/NgoạiLệCácCậnChuỗi";
        if (giáTrịCănCước == 32) return "tiếngViệt/tựThân/NgoạiLệThamChiếuRỗngThamChiếu";
        if (giáTrịCănCước == 33) return "tiếngViệt/tựThân/SựThấtBạiSốHọc";
        if (giáTrịCănCước == 34) return "tiếngViệt/tựThân/NgoạiLệTrạngThái";
        if (giáTrịCănCước == 35) return "tiếngViệt/tựThân/NgoạiLệÉpKiểuKiểu";
        if (giáTrịCănCước == 36) return "tiếngViệt/tựThân/SựThấtBạiCỡMảngÂm";
        if (giáTrịCănCước == 37) return "tiếngViệt/tựThân/SựThấtBạiCấtMảng";
        if (giáTrịCănCước == 38) return "tiếngViệt/tựThân/NgoạiLệTrạngTháiLuồngChạy";
        if (giáTrịCănCước == 1) return "java/lang/Throwable"; if (giáTrịCănCước == 2) return "java/lang/Exception";
        if (giáTrịCănCước == 3) return "java/lang/RuntimeException"; if (giáTrịCănCước == 4) return "java/lang/ArithmeticException";
        if (giáTrịCănCước == 5) return "java/lang/NullPointerException"; if (giáTrịCănCước == 6) return "java/lang/IndexOutOfBoundsException";
        if (giáTrịCănCước == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (giáTrịCănCước == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (giáTrịCănCước == 9) return "java/lang/IllegalArgumentException"; if (giáTrịCănCước == 10) return "java/lang/NumberFormatException";
        if (giáTrịCănCước == 11) return "java/io/IOException"; if (giáTrịCănCước == 12) return "java/io/FileNotFoundException";
        if (giáTrịCănCước == 17) return "java/lang/ArrayStoreException";
        if (giáTrịCănCước == 18) return "java/net/UnknownHostException";
        if (giáTrịCănCước == 19) return "java/net/SocketTimeoutException";
        if (giáTrịCănCước == 16) return "java/lang/IllegalThreadStateException";
        if (giáTrịCănCước == 13) return "java/lang/IllegalStateException"; if (giáTrịCănCước == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int chaNgoạiLệ(int giáTrịCănCước) {
        if (giáTrịCănCước == 40) return 2;
        if (giáTrịCănCước == 41) return 40;
        if (giáTrịCănCước == 39) return 11;
        if (giáTrịCănCước == 1) return 0;
        if (giáTrịCănCước == 2) return 1;
        if (giáTrịCănCước == 3) return 2;
        if (giáTrịCănCước == 4) return 3;
        if (giáTrịCănCước == 5) return 3;
        if (giáTrịCănCước == 6) return 3;
        if (giáTrịCănCước == 7) return 6;
        if (giáTrịCănCước == 8) return 6;
        if (giáTrịCănCước == 9) return 3;
        if (giáTrịCănCước == 10) return 9;
        if (giáTrịCănCước == 11) return 2;
        if (giáTrịCănCước == 12) return 11;
        if (giáTrịCănCước == 13) return 3;
        if (giáTrịCănCước == 14) return 3;
        if (giáTrịCănCước == 15) return 3;
        if (giáTrịCănCước == 16) return 9;
        if (giáTrịCănCước == 17) return 3;
        if (giáTrịCănCước == 18) return 11;
        if (giáTrịCănCước == 19) return 11;
        if (giáTrịCănCước == 20) return 2;
        if (giáTrịCănCước == 21) return 3;
        if (giáTrịCănCước == 22) return 11;
        if (giáTrịCănCước == 23) return 22;
        if (giáTrịCănCước == 24) return 22;
        if (giáTrịCănCước == 25) return 22;
        if (giáTrịCănCước == 26) return 22;
        if (giáTrịCănCước == 27) return 9;
        if (giáTrịCănCước == 28) return 27;
        if (giáTrịCănCước == 29) return 6;
        if (giáTrịCănCước == 30) return 29;
        if (giáTrịCănCước == 31) return 29;
        if (giáTrịCănCước == 32) return 5;
        if (giáTrịCănCước == 33) return 4;
        if (giáTrịCănCước == 34) return 13;
        if (giáTrịCănCước == 35) return 14;
        if (giáTrịCănCước == 36) return 15;
        if (giáTrịCănCước == 37) return 17;
        if (giáTrịCănCước == 38) return 16;
        return 0;
    }
    static boolean ngoạiLệChứa(int giáTrịThựcTế, int mongMuốn) {
        for (int giáTrịĐộSâu = 0; giáTrịThựcTế != 0 && giáTrịĐộSâu < 16; giáTrịĐộSâu++, giáTrịThựcTế = chaNgoạiLệ(giáTrịThựcTế))
            if (giáTrịThựcTế == mongMuốn) return true;
        return false;
    }
    static void némNgoạiLệ(int giáTrịCănCước, String thamChiếuHãyĐọc) {
        int thamChiếuĐốiTượng = bộNhớMới(9, 2); if (lỗi) return;
        giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2] = giáTrịCănCước; giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 3] = kýTựChủ(thamChiếuHãyĐọc); thamChiếuVùngNhớĐộng[thamChiếuĐốiTượng + 3] = 1;
        đốiTượngĐãNém = thamChiếuĐốiTượng; lỗi = true;
    }
    static boolean đốiTượngViệcSoKhớp(int thamChiếuĐốiTượng, int tên) {
        if (thamChiếuĐốiTượng == 0) return true;
        if (!làĐốiTượngHợpLệ(thamChiếuĐốiTượng)) return false;
        int mãLoạiMục = giáTrịVùngNhớĐộng[thamChiếuĐốiTượng];
        if (vănBảnTừ(tên, "java/lang/Object")) return true;
        if (mãLoạiMục >= 32) return lớpChứa(mãLoạiMục - 32, tên);
        if (mãLoạiMục == 9) { int địaChỉĐốiĐích = hằngNgoạiLệ(tên); return địaChỉĐốiĐích != 0 && ngoạiLệChứa(giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2], địaChỉĐốiĐích); }
        if (mãLoạiMục == 1) return vănBảnTừ(tên, "java/lang/String") || vănBảnTừ(tên, "java/lang/CharSequence");
        if (mãLoạiMục == 4) return vănBảnTừ(tên, "java/lang/StringBuilder") || vănBảnTừ(tên, "java/lang/CharSequence");
        if (mãLoạiMục == 10) return vănBảnTừ(tên, "java/util/ArrayList") || vănBảnTừ(tên, "java/util/List");
        if (mãLoạiMục == 11) return vănBảnTừ(tên, "java/util/HashMap") || vănBảnTừ(tên, "java/util/Map");
        if (mãLoạiMục == 12) return vănBảnTừ(tên, "java/lang/Integer") || vănBảnTừ(tên, "java/lang/Number");
        if (mãLoạiMục >= 24 && mãLoạiMục <= 28 && giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 13] != 0) return lớpMànHìnhTiếngHàn(tên) == mãLoạiMục || vănBảnTừ(tên, "tiếngViệt/tựThân/PhầnTửMànHình");
        if (mãLoạiMục >= 24 && mãLoạiMục <= 28) return (lớpMànHìnhTiếngHàn(tên) == 0 && lớpMànHình(tên) == mãLoạiMục) || vănBảnTừ(tên, "java/awt/Component") || vănBảnTừ(tên, "java/awt/Container") || vănBảnTừ(tên, "javax/swing/JComponent");
        if (mãLoạiMục == 29) return vănBảnTừ(tên, giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 3] != 0 ? "tiếngViệt/tựThân/ThôngBáoHànhĐộng" : "java/awt/event/ActionEvent");
        if (mãLoạiMục == 30) return vănBảnTừ(tên, "java/awt/FlowLayout") || vănBảnTừ(tên, "java/awt/LayoutManager");
        if (mãLoạiMục == 17) return vănBảnTừ(tên, "java/net/Socket");
        if (mãLoạiMục == 18) return vănBảnTừ(tên, "java/net/ServerSocket");
        if (mãLoạiMục == 19) return vănBảnTừ(tên, giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (mãLoạiMục == 14) return vănBảnTừ(tên, "java/net/InetAddress");
        if (mãLoạiMục == 15) return vănBảnTừ(tên, "java/net/DatagramSocket");
        if (mãLoạiMục == 16) return vănBảnTừ(tên, "java/net/DatagramPacket");
        if (mãLoạiMục == 13) return vănBảnTừ(tên, giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 3] != 0 ? "tiếngViệt/tựThân/bộLàmViệc" : "java/lang/Thread");
        if (mãLoạiMục == 2) return vănBảnTừ(tên, "[I"); if (mãLoạiMục == 20) return vănBảnTừ(tên, "[B"); if (mãLoạiMục == 21) return vănBảnTừ(tên, "[Z");
        if (mãLoạiMục == 22) return vănBảnTừ(tên, "[C"); if (mãLoạiMục == 23) return vănBảnTừ(tên, "[S");
        if (mãLoạiMục != 3) return false;
        if (vănBảnTừ(tên, "[Ljava/lang/Object;")) return true;
        int thànhPhần = phầnTửMảng[thamChiếuĐốiTượng];
        if (thànhPhần == -1) return vănBảnTừ(tên, "[Ljava/lang/String;") || vănBảnTừ(tên, "[Ljava/lang/CharSequence;");
        if (thànhPhần == 0) return false;
        if (soSánhCácLớpMảng(thànhPhần, tên)) return true;
        if ((vănBảnTừ(thànhPhần, "java/lang/String") || vănBảnTừ(thànhPhần, "java/lang/StringBuilder")) && vănBảnTừ(tên, "[Ljava/lang/CharSequence;")) return true;
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < sốLượngĐịnhNghĩaLớp; chỉSốVòngLặp++) if (từViệcSoKhớp(tênĐịnhNghĩaLớp[chỉSốVòngLặp], thànhPhần)) {
            for (int mãKýTự = chỉSốVòngLặp, độSâu = 0; mãKýTự >= 0 && độSâu < 16; độSâu++, mãKýTự = lớpCha(mãKýTự)) {
                if (soSánhCácLớpMảng(chaĐịnhNghĩaLớp[mãKýTự], tên)) return true;
                for (int vịTríPhíaTrong = 0; vịTríPhíaTrong < sốLượngGiaoDiệnLớp[mãKýTự]; vịTríPhíaTrong++) if (soSánhCácLớpMảng(giaoDiệnLớp[mãKýTự * 16 + vịTríPhíaTrong], tên)) return true;
            }
        }
        return false;
    }
    static boolean soSánhCácLớpMảng(int hằngTên, int bộMôTả) {
        int kiểmTraVịTrí = giáTrịĐầuTiênHằng[bộMôTả], sốLượngMục = giáTrịThứHaiHằng[bộMôTả];
        if (hằngTên == 0 || sốLượngMục < 4 || Tệp[kiểmTraVịTrí] != '[' || Tệp[kiểmTraVịTrí + 1] != 'L' || Tệp[kiểmTraVịTrí + sốLượngMục - 1] != ';' || giáTrịThứHaiHằng[hằngTên] != sốLượngMục - 3) return false;
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < sốLượngMục - 3; chỉSốVòngLặp++) if (Tệp[giáTrịĐầuTiênHằng[hằngTên] + chỉSốVòngLặp] != Tệp[kiểmTraVịTrí + 2 + chỉSốVòngLặp]) return false;
        return true;
    }
    static void ngoạiLệThẻXửLý() {
        if (đốiTượngĐãNém == 0) return;
        lỗi = false;
        while (chỉSốKhung >= luồngChạyHiệnTại * 32) {
            int chỉSốTệp = phươngThứcKhung[chỉSốKhung], đọcConTrỏVănBản = chỉLệnhKhung[chỉSốKhung];
            for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < bắtSốLượng; chỉSốVòngLặp++) if (bắtPhươngThức[chỉSốVòngLặp] == chỉSốTệp && đọcConTrỏVănBản >= bắtBắtChạy[chỉSốVòngLặp] && đọcConTrỏVănBản < bắtKếtThúc[chỉSốVòngLặp]
                && (bắtLớp[chỉSốVòngLặp] == 0 || đốiTượngViệcSoKhớp(đốiTượngĐãNém, bắtLớp[chỉSốVòngLặp]))) {
                vịTríKhung[chỉSốKhung] = bắtVịTrí[chỉSốVòngLặp]; ngănXếpKhung[chỉSốKhung] = 0; đặtGiáTrị(đốiTượngĐãNém, 2); đốiTượngĐãNém = 0; return;
            }
            if (khởiTạoKhung[chỉSốKhung] != 0) trạngTháiĐịnhNghĩaLớp[khởiTạoKhung[chỉSốKhung] - 1] = 3;
            if (khóaKhung[chỉSốKhung] != 0) { giảiPhóngKhóa(khóaKhung[chỉSốKhung]); khóaKhung[chỉSốKhung] = 0; }
            chỉSốKhung--;
        }
        NgườiDùng.ghi("Uncaught ");
        if (giáTrịVùngNhớĐộng[đốiTượngĐãNém] == 9) { NgườiDùng.ghi(tênNgoạiLệ(giáTrịVùngNhớĐộng[đốiTượngĐãNém + 2])); NgườiDùng.ghi(": "); ghiVănBản(giáTrịVùngNhớĐộng[đốiTượngĐãNém + 3]); }
        else NgườiDùng.ghi("user exception");
        NgườiDùng.ghiGiáTrịKýTự(10); đốiTượngĐãNém = 0; lỗi = true;
    }
    // Hiện JVM này chỉ cho phép phần tử ngăn xếp category-1 (int/reference).
    static void chỉLệnhNgănXếp(int mãLệnh) {
        int dữLiệuĐầuTiên = trừCácGiáTrị(0), địnhDạngĐầuTiên = kiểuTrảVề;
        if (mãLệnh == 87) return;
        if (mãLệnh == 89) { đặtGiáTrị(dữLiệuĐầuTiên, địnhDạngĐầuTiên); đặtGiáTrị(dữLiệuĐầuTiên, địnhDạngĐầuTiên); return; }
        int dữLiệuByte = trừCácGiáTrị(0), địnhDạngThứHai = kiểuTrảVề;
        if (mãLệnh == 88) return;
        if (mãLệnh == 90) { đặtGiáTrị(dữLiệuĐầuTiên, địnhDạngĐầuTiên); đặtGiáTrị(dữLiệuByte, địnhDạngThứHai); đặtGiáTrị(dữLiệuĐầuTiên, địnhDạngĐầuTiên); return; }
        if (mãLệnh == 92) { đặtGiáTrị(dữLiệuByte, địnhDạngThứHai); đặtGiáTrị(dữLiệuĐầuTiên, địnhDạngĐầuTiên); đặtGiáTrị(dữLiệuByte, địnhDạngThứHai); đặtGiáTrị(dữLiệuĐầuTiên, địnhDạngĐầuTiên); return; }
        if (mãLệnh == 95) { đặtGiáTrị(dữLiệuĐầuTiên, địnhDạngĐầuTiên); đặtGiáTrị(dữLiệuByte, địnhDạngThứHai); return; }
        int mãKýTự = trừCácGiáTrị(0), địnhDạngThứBa = kiểuTrảVề;
        if (mãLệnh == 91) { đặtGiáTrị(dữLiệuĐầuTiên, địnhDạngĐầuTiên); đặtGiáTrị(mãKýTự, địnhDạngThứBa); đặtGiáTrị(dữLiệuByte, địnhDạngThứHai); đặtGiáTrị(dữLiệuĐầuTiên, địnhDạngĐầuTiên); return; }
        if (mãLệnh == 93) { đặtGiáTrị(dữLiệuByte, địnhDạngThứHai); đặtGiáTrị(dữLiệuĐầuTiên, địnhDạngĐầuTiên); đặtGiáTrị(mãKýTự, địnhDạngThứBa); đặtGiáTrị(dữLiệuByte, địnhDạngThứHai); đặtGiáTrị(dữLiệuĐầuTiên, địnhDạngĐầuTiên); return; }
        int giáTrịỞCuối = trừCácGiáTrị(0), địnhDạngThứTư = kiểuTrảVề;
        đặtGiáTrị(dữLiệuByte, địnhDạngThứHai); đặtGiáTrị(dữLiệuĐầuTiên, địnhDạngĐầuTiên); đặtGiáTrị(giáTrịỞCuối, địnhDạngThứTư); đặtGiáTrị(mãKýTự, địnhDạngThứBa); đặtGiáTrị(dữLiệuByte, địnhDạngThứHai); đặtGiáTrị(dữLiệuĐầuTiên, địnhDạngĐầuTiên);
    }
    static void đốiTượngMới(int hằngTên, int điểmĐangBắtChạy) {
        int mãLoạiMục = 0, độDàiHợpLệ = 0, thamChiếuNgoạiLệ = hằngNgoạiLệ(hằngTên);
        if (vănBảnTừ(hằngTên, "java/lang/StringBuilder")) { mãLoạiMục = 4; độDàiHợpLệ = 1; }
        if (vănBảnTừ(hằngTên, "java/io/FileInputStream")) { mãLoạiMục = 5; độDàiHợpLệ = 2; }
        if (vănBảnTừ(hằngTên, "java/io/FileOutputStream")) { mãLoạiMục = 6; độDàiHợpLệ = 2; }
        if (thamChiếuNgoạiLệ != 0) { mãLoạiMục = 9; độDàiHợpLệ = 2; }
        if (vănBảnTừ(hằngTên, "java/util/ArrayList")) { mãLoạiMục = 10; độDàiHợpLệ = 2; }
        if (vănBảnTừ(hằngTên, "java/util/HashMap")) { mãLoạiMục = 11; độDàiHợpLệ = 2; }
        if (vănBảnTừ(hằngTên, "java/lang/Integer")) { mãLoạiMục = 12; độDàiHợpLệ = 1; }
        if (vănBảnTừ(hằngTên, "java/net/Socket")) { mãLoạiMục = 17; độDàiHợpLệ = 5; }
        if (vănBảnTừ(hằngTên, "java/net/ServerSocket")) { mãLoạiMục = 18; độDàiHợpLệ = 5; }
        if (vănBảnTừ(hằngTên, "java/net/DatagramSocket")) { mãLoạiMục = 15; độDàiHợpLệ = 3; }
        if (vănBảnTừ(hằngTên, "java/net/DatagramPacket")) { mãLoạiMục = 16; độDàiHợpLệ = 4; }
        if (vănBảnTừ(hằngTên, "java/lang/Thread") || vănBảnTừ(hằngTên, "tiếngViệt/tựThân/bộLàmViệc")) { mãLoạiMục = 13; độDàiHợpLệ = 2; }
        if (vănBảnTừ(hằngTên, "java/lang/Object")) { mãLoạiMục = 8; }
        if (mãLoạiMục == 0 && lớpMànHình(hằngTên) != 0) { mãLoạiMục = lớpMànHình(hằngTên); độDàiHợpLệ = 12; }
        if (mãLoạiMục == 0) {
            int mãKýTự = tìmĐịnhNghĩaLớp(hằngTên); if (mãKýTự < 0 || lỗi || !khởiTạo(mãKýTự, điểmĐangBắtChạy)) return;
            mãLoạiMục = 32 + mãKýTự; độDàiHợpLệ = sốLượngÔLớp[mãKýTự];
        }
        int thamChiếuĐốiTượng = cấpPhátLưuTrữ(mãLoạiMục, độDàiHợpLệ); if (lỗi) return;
        if (mãLoạiMục == 13 && vănBảnTừ(hằngTên, "tiếngViệt/tựThân/bộLàmViệc")) giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 3] = 1;
        if (mãLoạiMục >= 24 && mãLoạiMục <= 28 && lớpMànHìnhTiếngHàn(hằngTên) != 0) giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 13] = 1;
        if (mãLoạiMục == 5 || mãLoạiMục == 6 || mãLoạiMục == 15 || mãLoạiMục == 17 || mãLoạiMục == 18) giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2] = -1;
        if (mãLoạiMục == 9) giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2] = thamChiếuNgoạiLệ;
        đặtGiáTrị(thamChiếuĐốiTượng, 2);
    }
    static boolean bằngCácGiáTrị(int dữLiệuĐầuTiên, int dữLiệuByte) {
        if (dữLiệuĐầuTiên == dữLiệuByte) return true;
        if (dữLiệuĐầuTiên == 0 || dữLiệuByte == 0 || dữLiệuĐầuTiên < 0 || dữLiệuByte < 0 || dữLiệuĐầuTiên >= vịTríKếtThúcVùngNhớĐộng || dữLiệuByte >= vịTríKếtThúcVùngNhớĐộng) return false;
        if (giáTrịVùngNhớĐộng[dữLiệuĐầuTiên] == 1 && giáTrịVùngNhớĐộng[dữLiệuByte] == 1) return bằngCácVănBản(dữLiệuĐầuTiên, dữLiệuByte, false);
        return giáTrịVùngNhớĐộng[dữLiệuĐầuTiên] == 12 && giáTrịVùngNhớĐộng[dữLiệuByte] == 12 && giáTrịVùngNhớĐộng[dữLiệuĐầuTiên + 2] == giáTrịVùngNhớĐộng[dữLiệuByte + 2];
    }
    static int đoạnVănBản(int thamChiếuĐốiTượng, int bắtChạyVịTrí, int vịTríKếtThúc) {
        if (!giáTrịĐốiTượng(thamChiếuĐốiTượng, 1)) return 0;
        if (bắtChạyVịTrí < 0 || vịTríKếtThúc < bắtChạyVịTrí || vịTríKếtThúc > giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 1]) { giáTrịSựThấtBại("StringIndexOutOfBoundsException"); return 0; }
        int giáTrịĐãTrảVề = cấpPhátLưuTrữ(1, vịTríKếtThúc - bắtChạyVịTrí); if (lỗi) return 0;
        for (int chỉSốVòngLặp = bắtChạyVịTrí; chỉSốVòngLặp < vịTríKếtThúc; chỉSốVòngLặp++) giáTrịVùngNhớĐộng[giáTrịĐãTrảVề + 2 + chỉSốVòngLặp - bắtChạyVịTrí] = giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2 + chỉSốVòngLặp];
        return giáTrịĐãTrảVề;
    }
    static int nốiVănBản(int dữLiệuĐầuTiên, int dữLiệuByte) {
        if (!giáTrịĐốiTượng(dữLiệuĐầuTiên, 1) || !giáTrịĐốiTượng(dữLiệuByte, 1)) return 0;
        int sốLượngMục = giáTrịVùngNhớĐộng[dữLiệuĐầuTiên + 1], chỉSốPhươngThức = giáTrịVùngNhớĐộng[dữLiệuByte + 1], giáTrịĐãTrảVề = cấpPhátLưuTrữ(1, sốLượngMục + chỉSốPhươngThức); if (lỗi) return 0;
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < sốLượngMục; chỉSốVòngLặp++) giáTrịVùngNhớĐộng[giáTrịĐãTrảVề + 2 + chỉSốVòngLặp] = giáTrịVùngNhớĐộng[dữLiệuĐầuTiên + 2 + chỉSốVòngLặp];
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < chỉSốPhươngThức; chỉSốVòngLặp++) giáTrịVùngNhớĐộng[giáTrịĐãTrảVề + 2 + sốLượngMục + chỉSốVòngLặp] = giáTrịVùngNhớĐộng[dữLiệuByte + 2 + chỉSốVòngLặp];
        return giáTrịĐãTrảVề;
    }
    static boolean gọiThựcHiệnMặcĐịnh(int chủSởHữu, int hằngTên, int hằngBộMôTả, int mãLệnh) {
        if (vănBảnTừ(chủSởHữu, "tiếngViệt/tựThân/CácĐốiSố") && mãLệnh == 184) {
            if (vănBảnTừ(hằngTên, "sốLượngPhầnMục") && vănBảnTừ(hằngBộMôTả, "()I")) { đặtGiáTrị(NgườiDùng.sốLượngCácĐốiSố() - 1, 1); return true; }
            if (vănBảnTừ(hằngTên, "vănBản") && vănBảnTừ(hằngBộMôTả, "(I)Ljava/lang/String;")) {
                int chỉSốThứBậc = trừCácGiáTrị(1);
                if (chỉSốThứBậc < 0 || chỉSốThứBậc >= NgườiDùng.sốLượngCácĐốiSố() - 1) némNgoạiLệ(29, "thựcThiLệnh cácĐốiSố 범위를 벗어났습니다");
                else đặtGiáTrị(kýTựChủ(NgườiDùng.cácĐốiSố(chỉSốThứBậc + 1)), 2);
                return true;
            }
            giáTrịSựThấtBại("지원하지 않는 tiếngViệt thựcThiLệnh cácĐốiSố gọiThựcHiện"); return true;
        }
        if (vănBảnTừ(chủSởHữu, "tiếngViệt/tựThân/bộLàmViệc")) { luồngChạyTiếnTrình(hằngTên, hằngBộMôTả, mãLệnh, true); return true; }
        if (chủSởHữuMànHìnhTiếngHàn(chủSởHữu)) { gọiThựcHiệnMànHìnhTiếngHàn(chủSởHữu, hằngTên, hằngBộMôTả, mãLệnh); return true; }
        if (chủSởHữuMànHình(chủSởHữu)) { gọiThựcHiệnMànHình(chủSởHữu, hằngTên, hằngBộMôTả, mãLệnh); return true; }
        if (vănBảnTừ(chủSởHữu, "java/net/Socket") || vănBảnTừ(chủSởHữu, "java/net/ServerSocket") || vănBảnTừ(chủSởHữu, "java/io/InputStream") || vănBảnTừ(chủSởHữu, "java/io/OutputStream")) { gọiThựcHiệnLuồng(chủSởHữu, hằngTên, hằngBộMôTả, mãLệnh); return true; }
        if (vănBảnTừ(chủSởHữu, "tiếngViệt/tựThân/giáTrịNhân") && mãLệnh == 184) {
            if (vănBảnTừ(hằngTên, "rộngMànHình") && vănBảnTừ(hằngBộMôTả, "()I")) { đặtGiáTrị(NgườiDùng.rộngMànHình(), 1); return true; }
            if (vănBảnTừ(hằngTên, "caoMànHình") && vănBảnTừ(hằngBộMôTả, "()I")) { đặtGiáTrị(NgườiDùng.caoMànHình(), 1); return true; }
            if (vănBảnTừ(hằngTên, "miliGiây") && vănBảnTừ(hằngBộMôTả, "()I")) { đặtGiáTrị(NgườiDùng.miliGiây(), 1); return true; }
            if (vănBảnTừ(hằngTên, "chờẢnhCho") && vănBảnTừ(hằngBộMôTả, "()I")) { đặtGiáTrị(NgườiDùng.chờẢnhCho(), 1); return true; }
            if (vănBảnTừ(hằngTên, "hìnhChữNhật") && vănBảnTừ(hằngBộMôTả, "(IIIII)I")) { int màuĐiểmẢnh = trừCácGiáTrị(1), giáTrịCao = trừCácGiáTrị(1), giáTrịRộng = trừCácGiáTrị(1), tọaĐộY = trừCácGiáTrị(1), tọaĐộX = trừCácGiáTrị(1); đặtGiáTrị(NgườiDùng.hìnhChữNhật(tọaĐộX, tọaĐộY, giáTrịRộng, giáTrịCao, màuĐiểmẢnh), 1); return true; }
        }
        if (vănBảnTừ(chủSởHữu, "java/net/InetAddress") || vănBảnTừ(chủSởHữu, "java/net/DatagramPacket") || vănBảnTừ(chủSởHữu, "java/net/DatagramSocket")) { gọiThựcHiệnMạng(chủSởHữu, hằngTên, hằngBộMôTả, mãLệnh); return true; }
        if (vănBảnTừ(chủSởHữu, "java/lang/Thread")) { gọiThựcHiệnLuồngChạy(hằngTên, hằngBộMôTả, mãLệnh); return true; }
        if (vănBảnTừ(chủSởHữu, "java/lang/Object")) {
            if (vănBảnTừ(hằngTên, "<init>") && vănBảnTừ(hằngBộMôTả, "()V") && mãLệnh == 183) { làĐốiTượngHợpLệ(trừCácGiáTrị(2)); return true; }
            if (vănBảnTừ(hằngTên, "equals") && vănBảnTừ(hằngBộMôTả, "(Ljava/lang/Object;)Z")) { int dữLiệuByte = trừCácGiáTrị(2), dữLiệuĐầuTiên = trừCácGiáTrị(2); if (làĐốiTượngHợpLệ(dữLiệuĐầuTiên)) đặtGiáTrị(dữLiệuĐầuTiên == dữLiệuByte ? 1 : 0, 1); return true; }
        }
        if (hằngNgoạiLệ(chủSởHữu) != 0) {
            if (vănBảnTừ(hằngTên, "<init>") && mãLệnh == 183 && (vănBảnTừ(hằngBộMôTả, "()V") || vănBảnTừ(hằngBộMôTả, "(Ljava/lang/String;)V"))) {
                int dấuNhắc = vănBảnTừ(hằngBộMôTả, "()V") ? 0 : trừCácGiáTrị(2), thamChiếuĐốiTượng = trừCácGiáTrị(2);
                if (giáTrịĐốiTượng(thamChiếuĐốiTượng, 9)) { giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 3] = dấuNhắc; thamChiếuVùngNhớĐộng[thamChiếuĐốiTượng + 3] = 1; } return true;
            }
            if ((vănBảnTừ(hằngTên, "getMessage") || vănBảnTừ(hằngTên, "môTả")) && vănBảnTừ(hằngBộMôTả, "()Ljava/lang/String;")) { int thamChiếuĐốiTượng = trừCácGiáTrị(2); if (giáTrịĐốiTượng(thamChiếuĐốiTượng, 9)) đặtGiáTrị(giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 3], 2); return true; }
        }
        if (vănBảnTừ(chủSởHữu, "java/lang/String")) {
            if (mãLệnh == 182 && vănBảnTừ(hằngTên, "getBytes") && (vănBảnTừ(hằngBộMôTả, "()[B") || vănBảnTừ(hằngBộMôTả, "(Ljava/lang/String;)[B"))) {
                int tênBảngMã = vănBảnTừ(hằngBộMôTả, "()[B") ? 0 : trừCácGiáTrị(2), thamChiếuĐốiTượng = trừCácGiáTrị(2);
                if (!giáTrịĐốiTượng(thamChiếuĐốiTượng, 1)) return true;
                if (tênBảngMã != 0 && !bằngCácVănBản(tênBảngMã, kýTựChủ("UTF-8"), false) && !bằngCácVănBản(tênBảngMã, kýTựChủ("UTF8"), false) && !bằngCácVănBản(tênBảngMã, kýTựChủ("utf-8"), false)) { némNgoạiLệ(11, "only UTF-8 encoding is supported"); return true; }
                int sốLượngMục = giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 1], giáTrịĐãTrảVề = cấpPhátLưuTrữ(20, sốLượngMục * 3), sốLượngĐãDùng = 0; if (lỗi) return true;
                for (int vịTríPhíaTrong = 0; vịTríPhíaTrong < sốLượngMục; vịTríPhíaTrong++) {
                    int mãKýTự = giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2 + vịTríPhíaTrong];
                    if (mãKýTự >= 0xd800 && mãKýTự <= 0xdbff && vịTríPhíaTrong + 1 < sốLượngMục && giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 3 + vịTríPhíaTrong] >= 0xdc00 && giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 3 + vịTríPhíaTrong] <= 0xdfff) mãKýTự = 0x10000 + ((mãKýTự - 0xd800) << 10) + giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2 + ++vịTríPhíaTrong] - 0xdc00;
                    else if (mãKýTự >= 0xd800 && mãKýTự <= 0xdfff) mãKýTự = '?';
                    if (mãKýTự < 128) giáTrịVùngNhớĐộng[giáTrịĐãTrảVề + 2 + sốLượngĐãDùng++] = mãKýTự;
                    else { int sốLượngByte = mãKýTự < 2048 ? 2 : mãKýTự < 65536 ? 3 : 4; giáTrịVùngNhớĐộng[giáTrịĐãTrảVề + 2 + sốLượngĐãDùng++] = (byte)((sốLượngByte == 2 ? 192 : sốLượngByte == 3 ? 224 : 240) | mãKýTự >> (6 * (sốLượngByte - 1))); for (int vịTríPhépSoSánh = sốLượngByte - 1; vịTríPhépSoSánh > 0; vịTríPhépSoSánh--) giáTrịVùngNhớĐộng[giáTrịĐãTrảVề + 2 + sốLượngĐãDùng++] = (byte)(128 | mãKýTự >> (6 * (vịTríPhépSoSánh - 1)) & 63); }
                }
                giáTrịVùngNhớĐộng[giáTrịĐãTrảVề + 1] = sốLượngĐãDùng; đặtGiáTrị(giáTrịĐãTrảVề, 2); return true;
            }
            if (mãLệnh == 184 && vănBảnTừ(hằngTên, "valueOf") && vănBảnTừ(hằngBộMôTả, "(I)Ljava/lang/String;")) { đặtGiáTrị(kýTựChữSố(trừCácGiáTrị(1)), 2); return true; }
            if (mãLệnh != 182) return false;
            if (vănBảnTừ(hằngTên, "equals") && vănBảnTừ(hằngBộMôTả, "(Ljava/lang/Object;)Z")) { int dữLiệuByte = trừCácGiáTrị(2), dữLiệuĐầuTiên = trừCácGiáTrị(2); if (giáTrịĐốiTượng(dữLiệuĐầuTiên, 1)) đặtGiáTrị(bằngCácVănBản(dữLiệuĐầuTiên, dữLiệuByte, false) ? 1 : 0, 1); return true; }
            if (vănBảnTừ(hằngTên, "isEmpty") && vănBảnTừ(hằngBộMôTả, "()Z")) { int dữLiệuĐầuTiên = trừCácGiáTrị(2); if (giáTrịĐốiTượng(dữLiệuĐầuTiên, 1)) đặtGiáTrị(giáTrịVùngNhớĐộng[dữLiệuĐầuTiên + 1] == 0 ? 1 : 0, 1); return true; }
            if (vănBảnTừ(hằngTên, "substring") && (vănBảnTừ(hằngBộMôTả, "(I)Ljava/lang/String;") || vănBảnTừ(hằngBộMôTả, "(II)Ljava/lang/String;"))) {
                boolean giáTrịThứHai = vănBảnTừ(hằngBộMôTả, "(II)Ljava/lang/String;"); int vịTríKếtThúc = giáTrịThứHai ? trừCácGiáTrị(1) : 0, điểmĐangBắtChạy = trừCácGiáTrị(1), dữLiệuĐầuTiên = trừCácGiáTrị(2);
                if (giáTrịĐốiTượng(dữLiệuĐầuTiên, 1)) đặtGiáTrị(đoạnVănBản(dữLiệuĐầuTiên, điểmĐangBắtChạy, giáTrịThứHai ? vịTríKếtThúc : giáTrịVùngNhớĐộng[dữLiệuĐầuTiên + 1]), 2); return true;
            }
            if (vănBảnTừ(hằngTên, "concat") && vănBảnTừ(hằngBộMôTả, "(Ljava/lang/String;)Ljava/lang/String;")) { int dữLiệuByte = trừCácGiáTrị(2), dữLiệuĐầuTiên = trừCácGiáTrị(2); đặtGiáTrị(nốiVănBản(dữLiệuĐầuTiên, dữLiệuByte), 2); return true; }
            if (vănBảnTừ(hằngTên, "hashCode") && vănBảnTừ(hằngBộMôTả, "()I")) { int dữLiệuĐầuTiên = trừCácGiáTrị(2), giáTrịMãBăm = 0; if (giáTrịĐốiTượng(dữLiệuĐầuTiên, 1)) { for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < giáTrịVùngNhớĐộng[dữLiệuĐầuTiên + 1]; chỉSốVòngLặp++) giáTrịMãBăm = giáTrịMãBăm * 31 + giáTrịVùngNhớĐộng[dữLiệuĐầuTiên + 2 + chỉSốVòngLặp]; đặtGiáTrị(giáTrịMãBăm, 1); } return true; }
            if (vănBảnTừ(hằngTên, "toString") && vănBảnTừ(hằngBộMôTả, "()Ljava/lang/String;")) { int dữLiệuĐầuTiên = trừCácGiáTrị(2); if (giáTrịĐốiTượng(dữLiệuĐầuTiên, 1)) đặtGiáTrị(dữLiệuĐầuTiên, 2); return true; }
        }
        if (vănBảnTừ(chủSởHữu, "java/lang/Integer")) {
            if (mãLệnh == 184 && vănBảnTừ(hằngTên, "valueOf") && vănBảnTừ(hằngBộMôTả, "(I)Ljava/lang/Integer;")) { int giáTrịDữLiệu = trừCácGiáTrị(1), thamChiếuĐốiTượng = giáTrịDữLiệu >= -128 && giáTrịDữLiệu <= 127 ? sốNguyênCất[giáTrịDữLiệu + 128] : 0; if (thamChiếuĐốiTượng == 0) { thamChiếuĐốiTượng = cấpPhátLưuTrữ(12, 1); if (!lỗi) { giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2] = giáTrịDữLiệu; if (giáTrịDữLiệu >= -128 && giáTrịDữLiệu <= 127) sốNguyênCất[giáTrịDữLiệu + 128] = thamChiếuĐốiTượng; } } đặtGiáTrị(thamChiếuĐốiTượng, 2); return true; }
            if (mãLệnh == 183 && vănBảnTừ(hằngTên, "<init>") && vănBảnTừ(hằngBộMôTả, "(I)V")) { int giáTrịDữLiệu = trừCácGiáTrị(1), thamChiếuĐốiTượng = trừCácGiáTrị(2); if (giáTrịĐốiTượng(thamChiếuĐốiTượng, 12)) giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2] = giáTrịDữLiệu; return true; }
            if (mãLệnh == 182 && vănBảnTừ(hằngTên, "intValue") && vănBảnTừ(hằngBộMôTả, "()I")) { int thamChiếuĐốiTượng = trừCácGiáTrị(2); if (giáTrịĐốiTượng(thamChiếuĐốiTượng, 12)) đặtGiáTrị(giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2], 1); return true; }
            if (mãLệnh == 184 && vănBảnTừ(hằngTên, "toString") && vănBảnTừ(hằngBộMôTả, "(I)Ljava/lang/String;")) { đặtGiáTrị(kýTựChữSố(trừCácGiáTrị(1)), 2); return true; }
        }
        if (vănBảnTừ(chủSởHữu, "java/lang/Math") && mãLệnh == 184) {
            if (vănBảnTừ(hằngTên, "abs") && vănBảnTừ(hằngBộMôTả, "(I)I")) { int đọcGiáTrị = trừCácGiáTrị(1); đặtGiáTrị(đọcGiáTrị < 0 ? -đọcGiáTrị : đọcGiáTrị, 1); return true; }
            if ((vănBảnTừ(hằngTên, "min") || vănBảnTừ(hằngTên, "max")) && vănBảnTừ(hằngBộMôTả, "(II)I")) { int dữLiệuByte = trừCácGiáTrị(1), dữLiệuĐầuTiên = trừCácGiáTrị(1); đặtGiáTrị(vănBảnTừ(hằngTên, "min") ? (dữLiệuĐầuTiên < dữLiệuByte ? dữLiệuĐầuTiên : dữLiệuByte) : (dữLiệuĐầuTiên > dữLiệuByte ? dữLiệuĐầuTiên : dữLiệuByte), 1); return true; }
        }
        if (vănBảnTừ(chủSởHữu, "java/lang/System") && mãLệnh == 184) {
            if (vănBảnTừ(hằngTên, "gc") && vănBảnTừ(hằngBộMôTả, "()V")) { thuThậpRác(); return true; }
            if (vănBảnTừ(hằngTên, "arraycopy") && vănBảnTừ(hằngBộMôTả, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int sốLượngMục = trừCácGiáTrị(1), chỉSốGiáTrịĐích = trừCácGiáTrị(1), dữLiệuByte = trừCácGiáTrị(2), bắtChạyVịTrí = trừCácGiáTrị(1), dữLiệuĐầuTiên = trừCácGiáTrị(2);
                if (làĐốiTượngHợpLệ(dữLiệuĐầuTiên) && làĐốiTượngHợpLệ(dữLiệuByte)) {
                    int mãLoạiMục = giáTrịVùngNhớĐộng[dữLiệuĐầuTiên];
                    if (giáTrịVùngNhớĐộng[dữLiệuByte] != mãLoạiMục || (mãLoạiMục != 2 && mãLoạiMục != 3 && (mãLoạiMục < 20 || mãLoạiMục > 23))) giáTrịSựThấtBại("arraycopy type mismatch");
                    else if (sốLượngMục < 0 || bắtChạyVịTrí < 0 || chỉSốGiáTrịĐích < 0 || bắtChạyVịTrí > giáTrịVùngNhớĐộng[dữLiệuĐầuTiên + 1] - sốLượngMục || chỉSốGiáTrịĐích > giáTrịVùngNhớĐộng[dữLiệuByte + 1] - sốLượngMục) giáTrịSựThấtBại("ArrayIndexOutOfBoundsException");
                    else if (dữLiệuĐầuTiên == dữLiệuByte && chỉSốGiáTrịĐích > bắtChạyVịTrí) { for (int chỉSốVòngLặp = sốLượngMục - 1; chỉSốVòngLặp >= 0; chỉSốVòngLặp--) giáTrịVùngNhớĐộng[dữLiệuByte + 2 + chỉSốGiáTrịĐích + chỉSốVòngLặp] = giáTrịVùngNhớĐộng[dữLiệuĐầuTiên + 2 + bắtChạyVịTrí + chỉSốVòngLặp]; }
                    else { for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < sốLượngMục && !lỗi; chỉSốVòngLặp++) { int giáTrịDữLiệu = giáTrịVùngNhớĐộng[dữLiệuĐầuTiên + 2 + bắtChạyVịTrí + chỉSốVòngLặp]; if (mãLoạiMục != 3 || cóThểMảngCất(dữLiệuByte, giáTrịDữLiệu)) giáTrịVùngNhớĐộng[dữLiệuByte + 2 + chỉSốGiáTrịĐích + chỉSốVòngLặp] = giáTrịDữLiệu; } }
                }
                return true;
            }
        }
        if (vănBảnTừ(chủSởHữu, "java/util/ArrayList") || vănBảnTừ(chủSởHữu, "java/util/List") || vănBảnTừ(chủSởHữu, "java/util/HashMap") || vănBảnTừ(chủSởHữu, "java/util/Map")) {
            gọiThựcHiệnTậpHợp(chủSởHữu, hằngTên, hằngBộMôTả, mãLệnh); return true;
        }
        return false;
    }
    static void mởRộngTậpHợp(int thamChiếuĐốiTượng, int sốLượngBắtBuộc) {
        int giáTrịTrướcĐó = giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2], dữLiệuSứcChứa = giáTrịTrướcĐó == 0 ? 0 : giáTrịVùngNhớĐộng[giáTrịTrướcĐó + 1];
        if (dữLiệuSứcChứa >= sốLượngBắtBuộc) return;
        int vịTríKếTiếp = dữLiệuSứcChứa < 8 ? 8 : dữLiệuSứcChứa * 2; if (vịTríKếTiếp < sốLượngBắtBuộc) vịTríKếTiếp = sốLượngBắtBuộc;
        int mảngDữLiệu = cấpPhátLưuTrữ(3, vịTríKếTiếp); if (lỗi) return;
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < dữLiệuSứcChứa; chỉSốVòngLặp++) giáTrịVùngNhớĐộng[mảngDữLiệu + 2 + chỉSốVòngLặp] = giáTrịVùngNhớĐộng[giáTrịTrướcĐó + 2 + chỉSốVòngLặp];
        giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2] = mảngDữLiệu; thamChiếuVùngNhớĐộng[thamChiếuĐốiTượng + 2] = 1;
    }
    static void gọiThựcHiệnTậpHợp(int chủSởHữu, int hằngTên, int hằngBộMôTả, int mãLệnh) {
        boolean thamChiếuĐãÁnhXạ = vănBảnTừ(chủSởHữu, "java/util/HashMap") || vănBảnTừ(chủSởHữu, "java/util/Map"); int mãLoạiMục = thamChiếuĐãÁnhXạ ? 11 : 10;
        if (vănBảnTừ(hằngTên, "<init>") && mãLệnh == 183 && vănBảnTừ(hằngBộMôTả, "()V")) { int thamChiếuĐốiTượng = trừCácGiáTrị(2); if (giáTrịĐốiTượng(thamChiếuĐốiTượng, mãLoạiMục)) mởRộngTậpHợp(thamChiếuĐốiTượng, 8); return; }
        if (mãLệnh != 182 && mãLệnh != 185) { giáTrịSựThấtBại("invalid collection invocation"); return; }
        if (vănBảnTừ(hằngTên, "size") && vănBảnTừ(hằngBộMôTả, "()I") || vănBảnTừ(hằngTên, "isEmpty") && vănBảnTừ(hằngBộMôTả, "()Z")) {
            int thamChiếuĐốiTượng = trừCácGiáTrị(2); if (giáTrịĐốiTượng(thamChiếuĐốiTượng, mãLoạiMục)) đặtGiáTrị(vănBảnTừ(hằngTên, "size") ? giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 3] : giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 3] == 0 ? 1 : 0, 1); return;
        }
        if (vănBảnTừ(hằngTên, "clear") && vănBảnTừ(hằngBộMôTả, "()V")) { int thamChiếuĐốiTượng = trừCácGiáTrị(2); if (giáTrịĐốiTượng(thamChiếuĐốiTượng, mãLoạiMục)) { int mảngDữLiệu = giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2]; for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < giáTrịVùngNhớĐộng[mảngDữLiệu + 1]; chỉSốVòngLặp++) giáTrịVùngNhớĐộng[mảngDữLiệu + 2 + chỉSốVòngLặp] = 0; giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 3] = 0; } return; }
        if (!thamChiếuĐãÁnhXạ && vănBảnTừ(hằngTên, "add") && vănBảnTừ(hằngBộMôTả, "(Ljava/lang/Object;)Z")) {
            int giáTrịDữLiệu = trừCácGiáTrị(2), thamChiếuĐốiTượng = trừCácGiáTrị(2); if (!giáTrịĐốiTượng(thamChiếuĐốiTượng, 10)) return;
            int sốLượngMục = giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 3]; mởRộngTậpHợp(thamChiếuĐốiTượng, sốLượngMục + 1); if (!lỗi) { giáTrịVùngNhớĐộng[giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2] + 2 + sốLượngMục] = giáTrịDữLiệu; giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 3] = sốLượngMục + 1; đặtGiáTrị(1, 1); } return;
        }
        if (!thamChiếuĐãÁnhXạ && (vănBảnTừ(hằngTên, "get") || vănBảnTừ(hằngTên, "remove")) && vănBảnTừ(hằngBộMôTả, "(I)Ljava/lang/Object;") || !thamChiếuĐãÁnhXạ && vănBảnTừ(hằngTên, "set") && vănBảnTừ(hằngBộMôTả, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean làĐãGán = vănBảnTừ(hằngTên, "set"); int giáTrịDữLiệu = làĐãGán ? trừCácGiáTrị(2) : 0, vịTríMục = trừCácGiáTrị(1), thamChiếuĐốiTượng = trừCácGiáTrị(2);
            if (!giáTrịĐốiTượng(thamChiếuĐốiTượng, 10)) return;
            int sốLượngMục = giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 3], mảngDữLiệu = giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2];
            if (vịTríMục < 0 || vịTríMục >= sốLượngMục) { némNgoạiLệ(6, "list index"); return; }
            int giáTrịTrướcĐó = giáTrịVùngNhớĐộng[mảngDữLiệu + 2 + vịTríMục];
            if (làĐãGán) giáTrịVùngNhớĐộng[mảngDữLiệu + 2 + vịTríMục] = giáTrịDữLiệu;
            if (vănBảnTừ(hằngTên, "remove")) { for (int chỉSốVòngLặp = vịTríMục + 1; chỉSốVòngLặp < sốLượngMục; chỉSốVòngLặp++) giáTrịVùngNhớĐộng[mảngDữLiệu + 1 + chỉSốVòngLặp] = giáTrịVùngNhớĐộng[mảngDữLiệu + 2 + chỉSốVòngLặp]; giáTrịVùngNhớĐộng[mảngDữLiệu + 1 + sốLượngMục] = 0; giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 3] = sốLượngMục - 1; }
            đặtGiáTrị(giáTrịTrướcĐó, 2); return;
        }
        if (thamChiếuĐãÁnhXạ && (vănBảnTừ(hằngTên, "get") || vănBảnTừ(hằngTên, "remove")) && vănBảnTừ(hằngBộMôTả, "(Ljava/lang/Object;)Ljava/lang/Object;") || thamChiếuĐãÁnhXạ && vănBảnTừ(hằngTên, "put") && vănBảnTừ(hằngBộMôTả, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || thamChiếuĐãÁnhXạ && vănBảnTừ(hằngTên, "containsKey") && vănBảnTừ(hằngBộMôTả, "(Ljava/lang/Object;)Z")) {
            boolean làPhépChèn = vănBảnTừ(hằngTên, "put"), gỡ = vănBảnTừ(hằngTên, "remove");
            int giáTrịDữLiệu = làPhépChèn ? trừCácGiáTrị(2) : 0, thamChiếuPhím = trừCácGiáTrị(2), thamChiếuĐốiTượng = trừCácGiáTrị(2); if (!giáTrịĐốiTượng(thamChiếuĐốiTượng, 11)) return;
            int sốLượngMục = giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 3], mảngDữLiệu = giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2], đãTìmThấyĐãLà = -1;
            for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < sốLượngMục; chỉSốVòngLặp++) if (bằngCácGiáTrị(thamChiếuPhím, giáTrịVùngNhớĐộng[mảngDữLiệu + 2 + 2 * chỉSốVòngLặp])) { đãTìmThấyĐãLà = chỉSốVòngLặp; break; }
            int giáTrịTrướcĐó = đãTìmThấyĐãLà < 0 ? 0 : giáTrịVùngNhớĐộng[mảngDữLiệu + 3 + 2 * đãTìmThấyĐãLà];
            if (làPhépChèn) {
                if (đãTìmThấyĐãLà < 0) { mởRộngTậpHợp(thamChiếuĐốiTượng, (sốLượngMục + 1) * 2); mảngDữLiệu = giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2]; đãTìmThấyĐãLà = sốLượngMục; if (!lỗi) giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 3] = sốLượngMục + 1; }
                if (!lỗi) { giáTrịVùngNhớĐộng[mảngDữLiệu + 2 + 2 * đãTìmThấyĐãLà] = thamChiếuPhím; giáTrịVùngNhớĐộng[mảngDữLiệu + 3 + 2 * đãTìmThấyĐãLà] = giáTrịDữLiệu; }
            }
            if (gỡ && đãTìmThấyĐãLà >= 0) { for (int chỉSốVòngLặp = đãTìmThấyĐãLà + 1; chỉSốVòngLặp < sốLượngMục; chỉSốVòngLặp++) { giáTrịVùngNhớĐộng[mảngDữLiệu + 2 * chỉSốVòngLặp] = giáTrịVùngNhớĐộng[mảngDữLiệu + 2 + 2 * chỉSốVòngLặp]; giáTrịVùngNhớĐộng[mảngDữLiệu + 1 + 2 * chỉSốVòngLặp] = giáTrịVùngNhớĐộng[mảngDữLiệu + 3 + 2 * chỉSốVòngLặp]; } giáTrịVùngNhớĐộng[mảngDữLiệu + 2 * sốLượngMục] = 0; giáTrịVùngNhớĐộng[mảngDữLiệu + 1 + 2 * sốLượngMục] = 0; giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 3] = sốLượngMục - 1; }
            if (vănBảnTừ(hằngTên, "containsKey")) đặtGiáTrị(đãTìmThấyĐãLà >= 0 ? 1 : 0, 1); else đặtGiáTrị(giáTrịTrướcĐó, 2);
            return;
        }
        giáTrịSựThấtBại("unsupported collection method");
    }
    static boolean thuNhậnKhóa(int thamChiếuĐốiTượng) {
        if (!làĐốiTượngHợpLệ(thamChiếuĐốiTượng)) return false;
        if (độSâuKhóa[thamChiếuĐốiTượng] != 0 && chủSởHữuKhóa[thamChiếuĐốiTượng] != luồngChạyHiệnTại + 1) { đổiYêuCầu = true; return false; }
        chủSởHữuKhóa[thamChiếuĐốiTượng] = luồngChạyHiệnTại + 1; độSâuKhóa[thamChiếuĐốiTượng]++; return true;
    }
    static void giảiPhóngKhóa(int thamChiếuĐốiTượng) {
        if (!làĐốiTượngHợpLệ(thamChiếuĐốiTượng)) return;
        if (độSâuKhóa[thamChiếuĐốiTượng] == 0 || chủSởHữuKhóa[thamChiếuĐốiTượng] != luồngChạyHiệnTại + 1) { némNgoạiLệ(13, "monitor not owned"); return; }
        if (--độSâuKhóa[thamChiếuĐốiTượng] == 0) chủSởHữuKhóa[thamChiếuĐốiTượng] = 0;
    }
    static boolean luồngChạyChuyển() {
        khungLuồngChạy[luồngChạyHiệnTại] = chỉSốKhung;
        if (chỉSốKhung < luồngChạyHiệnTại * 32) trạngTháiLuồngChạy[luồngChạyHiệnTại] = 3;
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < sốLượngLuồngChạy; chỉSốVòngLặp++) if (trạngTháiLuồngChạy[chỉSốVòngLặp] == 2 && trạngTháiLuồngChạy[chờLuồngChạyCho[chỉSốVòngLặp]] == 3) trạngTháiLuồngChạy[chỉSốVòngLặp] = 1;
        for (int chỉSốVòngLặp = 1; chỉSốVòngLặp <= sốLượngLuồngChạy; chỉSốVòngLặp++) {
            int vịTríKếTiếp = (luồngChạyHiệnTại + chỉSốVòngLặp) % sốLượngLuồngChạy;
            if (trạngTháiLuồngChạy[vịTríKếTiếp] == 1) { luồngChạyHiệnTại = vịTríKếTiếp; chỉSốKhung = khungLuồngChạy[vịTríKếTiếp]; đổiYêuCầu = false; return true; }
        }
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < sốLượngLuồngChạy; chỉSốVòngLặp++) if (trạngTháiLuồngChạy[chỉSốVòngLặp] != 3) { giáTrịSựThấtBại("thread deadlock"); return false; }
        return false;
    }
    static void gọiThựcHiệnLuồngChạy(int hằngTên, int hằngBộMôTả, int mãLệnh) { luồngChạyTiếnTrình(hằngTên, hằngBộMôTả, mãLệnh, false); }
    static void luồngChạyTiếnTrình(int hằngTên, int hằngBộMôTả, int mãLệnh, boolean tiếngViệt) {
        if (mãLệnh == 184 && vănBảnTừ(hằngTên, tiếngViệt ? "nhườngTácVụ" : "yield") && vănBảnTừ(hằngBộMôTả, "()V")) { đổiYêuCầu = true; return; }
        if (mãLệnh == 184 && vănBảnTừ(hằngTên, "currentThread") && vănBảnTừ(hằngBộMôTả, "()Ljava/lang/Thread;")) { đặtGiáTrị(đốiTượngLuồngChạy[luồngChạyHiệnTại], 2); return; }
        if (mãLệnh == 183 && vănBảnTừ(hằngTên, "<init>") && (vănBảnTừ(hằngBộMôTả, "()V") || vănBảnTừ(hằngBộMôTả, tiếngViệt ? "(LtiếngViệt/tựThân/TácVụChạyĐược;)V" : "(Ljava/lang/Runnable;)V"))) {
            int địaChỉĐốiĐích = vănBảnTừ(hằngBộMôTả, "()V") ? 0 : trừCácGiáTrị(2), thamChiếuĐốiTượng = trừCácGiáTrị(2);
            if (!làĐốiTượngHợpLệ(thamChiếuĐốiTượng)) return;
            if (giáTrịVùngNhớĐộng[thamChiếuĐốiTượng] == 13) { giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2] = địaChỉĐốiĐích; thamChiếuVùngNhớĐộng[thamChiếuĐốiTượng + 2] = 1; }
            else if (địaChỉĐốiĐích != 0) giáTrịSựThấtBại("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (mãLệnh == 182 && (vănBảnTừ(hằngTên, tiếngViệt ? "bắtChạyTácVụ" : "start") || vănBảnTừ(hằngTên, tiếngViệt ? "đợi" : "join")) && vănBảnTừ(hằngBộMôTả, "()V") || mãLệnh == 182 && vănBảnTừ(hằngTên, tiếngViệt ? "làCònSống" : "isAlive") && vănBảnTừ(hằngBộMôTả, "()Z")) {
            int thamChiếuĐốiTượng = trừCácGiáTrị(2); if (!làĐốiTượngHợpLệ(thamChiếuĐốiTượng)) return;
            int giáTrịCănCước = -1; for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < sốLượngLuồngChạy; chỉSốVòngLặp++) if (đốiTượngLuồngChạy[chỉSốVòngLặp] == thamChiếuĐốiTượng) giáTrịCănCước = chỉSốVòngLặp;
            if (vănBảnTừ(hằngTên, tiếngViệt ? "làCònSống" : "isAlive")) { đặtGiáTrị(giáTrịCănCước >= 0 && trạngTháiLuồngChạy[giáTrịCănCước] != 3 ? 1 : 0, 1); return; }
            if (vănBảnTừ(hằngTên, tiếngViệt ? "đợi" : "join")) { if (giáTrịCănCước >= 0 && trạngTháiLuồngChạy[giáTrịCănCước] != 3) { chờLuồngChạyCho[luồngChạyHiệnTại] = giáTrịCănCước; trạngTháiLuồngChạy[luồngChạyHiệnTại] = 2; đổiYêuCầu = true; } return; }
            if (giáTrịCănCước >= 0) { némNgoạiLệ(tiếngViệt ? 38 : 16, "thread already started"); return; }
            if (sốLượngLuồngChạy == 4) { giáTrịSựThấtBại("thread limit (4 including main)"); return; }
            int địaChỉĐốiĐích = giáTrịVùngNhớĐộng[thamChiếuĐốiTượng] == 13 ? giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2] : thamChiếuĐốiTượng;
            int chỉSốTệp = địaChỉĐốiĐích > 0 && giáTrịVùngNhớĐộng[địaChỉĐốiĐích] >= 32 ? phươngThứcTên(giáTrịVùngNhớĐộng[địaChỉĐốiĐích] - 32, tiếngViệt ? "thựcThiTácVụ" : "run", "()V") : -1;
            if (địaChỉĐốiĐích != 0 && chỉSốTệp < 0) { giáTrịSựThấtBại("Runnable.run required"); return; }
            giáTrịCănCước = sốLượngLuồngChạy++; đốiTượngLuồngChạy[giáTrịCănCước] = thamChiếuĐốiTượng; đốiĐíchLuồngChạy[giáTrịCănCước] = địaChỉĐốiĐích;
            int khung = giáTrịCănCước * 32; khungLuồngChạy[giáTrịCănCước] = chỉSốTệp < 0 ? khung - 1 : khung; trạngTháiLuồngChạy[giáTrịCănCước] = chỉSốTệp < 0 ? 3 : 1;
            if (chỉSốTệp >= 0) { phươngThứcKhung[khung] = chỉSốTệp; vịTríKhung[khung] = bắtChạyPhươngThức[chỉSốTệp]; giáTrịCụcBộ[khung * 128] = địaChỉĐốiĐích; kiểuCụcBộ[khung * 128] = 2; }
            return;
        }
        giáTrịSựThấtBại("unsupported Thread method");
    }
    static int[] giáTrịTạmMạng = new int[514], vănBảnĐịaChỉ = new int[16];
    static int địaChỉCụcBộ() { return đốiTượngĐịaChỉ(0x7f000001); }
    static int đốiTượngĐịaChỉ(int giáTrị) { int thamChiếuĐốiTượng = cấpPhátLưuTrữ(14, 1); if (!lỗi) giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2] = giáTrị; return thamChiếuĐốiTượng; }
    static int giảiMãĐịaChỉ(int thamChiếuĐốiTượng) {
        if (thamChiếuĐốiTượng == 0 || bằngCácVănBản(thamChiếuĐốiTượng, kýTựChủ("localhost"), false)) return 0x7f000001;
        if (!giáTrịĐốiTượng(thamChiếuĐốiTượng, 1)) return 0;
        int giáTrịDữLiệu = 0, sốLượngTổngCộng = 0, byteĐịaChỉ = 0, cácChữSố = 0, sốLượngMục = giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 1];
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp <= sốLượngMục; chỉSốVòngLặp++) {
            int mãKýTự = chỉSốVòngLặp == sốLượngMục ? '.' : giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2 + chỉSốVòngLặp];
            if (mãKýTự == '.') { if (cácChữSố == 0 || sốLượngTổngCộng == 4) { némNgoạiLệ(18, "numeric IPv4 address required; DNS unavailable"); return 0; } giáTrịDữLiệu = giáTrịDữLiệu << 8 | byteĐịaChỉ; sốLượngTổngCộng++; byteĐịaChỉ = cácChữSố = 0; }
            else { if (mãKýTự < '0' || mãKýTự > '9' || ++cácChữSố > 3 || (byteĐịaChỉ = byteĐịaChỉ * 10 + mãKýTự - '0') > 255) { némNgoạiLệ(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (sốLượngTổngCộng != 4) { némNgoạiLệ(18, "invalid IPv4 address"); return 0; } return giáTrịDữLiệu;
    }
    static int kýTựĐịaChỉ(int giáTrịDữLiệu) {
        int sốLượngMục = 0;
        for (int dịch = 24; dịch >= 0; dịch -= 8) {
            int byteĐịaChỉ = giáTrịDữLiệu >>> dịch & 255;
            if (byteĐịaChỉ >= 100) vănBảnĐịaChỉ[sốLượngMục++] = '0' + byteĐịaChỉ / 100;
            if (byteĐịaChỉ >= 10) vănBảnĐịaChỉ[sốLượngMục++] = '0' + byteĐịaChỉ / 10 % 10;
            vănBảnĐịaChỉ[sốLượngMục++] = '0' + byteĐịaChỉ % 10; if (dịch != 0) vănBảnĐịaChỉ[sốLượngMục++] = '.';
        }
        int thamChiếuĐốiTượng = cấpPhátLưuTrữ(1, sốLượngMục); if (!lỗi) for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < sốLượngMục; chỉSốVòngLặp++) giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2 + chỉSốVòngLặp] = vănBảnĐịaChỉ[chỉSốVòngLặp]; return thamChiếuĐốiTượng;
    }
    static void gọiThựcHiệnMạng(int chủSởHữu, int hằngTên, int hằngBộMôTả, int mãLệnh) {
        if (vănBảnTừ(chủSởHữu, "java/net/InetAddress")) {
            if (mãLệnh == 184 && vănBảnTừ(hằngTên, "getLoopbackAddress") && vănBảnTừ(hằngBộMôTả, "()Ljava/net/InetAddress;")) { đặtGiáTrị(địaChỉCụcBộ(), 2); return; }
            if (mãLệnh == 184 && vănBảnTừ(hằngTên, "getByName") && vănBảnTừ(hằngBộMôTả, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int giáTrịDữLiệu = giảiMãĐịaChỉ(trừCácGiáTrị(2)); if (đốiTượngĐãNém == 0 && !lỗi) đặtGiáTrị(đốiTượngĐịaChỉ(giáTrịDữLiệu), 2); return;
            }
            if (mãLệnh == 182 && vănBảnTừ(hằngTên, "getHostAddress") && vănBảnTừ(hằngBộMôTả, "()Ljava/lang/String;")) { int thamChiếuĐốiTượng = trừCácGiáTrị(2); if (giáTrịĐốiTượng(thamChiếuĐốiTượng, 14)) đặtGiáTrị(kýTựĐịaChỉ(giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2]), 2); return; }
        }
        if (vănBảnTừ(chủSởHữu, "java/net/DatagramPacket")) {
            if (mãLệnh == 183 && vănBảnTừ(hằngTên, "<init>") && (vănBảnTừ(hằngBộMôTả, "([BI)V") || vănBảnTừ(hằngBộMôTả, "([BILjava/net/InetAddress;I)V"))) {
                boolean thamChiếuGiáTrịĐích = vănBảnTừ(hằngBộMôTả, "([BILjava/net/InetAddress;I)V"); int sốCổng = thamChiếuGiáTrịĐích ? trừCácGiáTrị(1) : 0, thamChiếuĐịaChỉ = thamChiếuGiáTrịĐích ? trừCácGiáTrị(2) : 0;
                int sốLượngMục = trừCácGiáTrị(1), mảngDữLiệu = trừCácGiáTrị(2), thamChiếuĐốiTượng = trừCácGiáTrị(2);
                if (!giáTrịĐốiTượng(thamChiếuĐốiTượng, 16) || !giáTrịĐốiTượng(mảngDữLiệu, 20)) return;
                if (sốLượngMục < 0 || sốLượngMục > giáTrịVùngNhớĐộng[mảngDữLiệu + 1] || sốCổng < 0 || sốCổng > 65535) { némNgoạiLệ(9, "invalid datagram length/port"); return; }
                if (thamChiếuĐịaChỉ != 0 && !giáTrịĐốiTượng(thamChiếuĐịaChỉ, 14)) return;
                giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2] = mảngDữLiệu; thamChiếuVùngNhớĐộng[thamChiếuĐốiTượng + 2] = 1; giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 3] = sốLượngMục;
                giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 4] = thamChiếuĐịaChỉ; thamChiếuVùngNhớĐộng[thamChiếuĐốiTượng + 4] = 1; giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 5] = sốCổng; return;
            }
            if (mãLệnh == 182 && vănBảnTừ(hằngTên, "setLength") && vănBảnTừ(hằngBộMôTả, "(I)V")) {
                int sốLượngMục = trừCácGiáTrị(1), thamChiếuĐốiTượng = trừCácGiáTrị(2); if (!giáTrịĐốiTượng(thamChiếuĐốiTượng, 16)) return;
                if (sốLượngMục < 0 || sốLượngMục > giáTrịVùngNhớĐộng[giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2] + 1]) némNgoạiLệ(9, "invalid datagram length"); else giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 3] = sốLượngMục; return;
            }
            if (mãLệnh == 182 && (vănBảnTừ(hằngTên, "getData") && vănBảnTừ(hằngBộMôTả, "()[B") || vănBảnTừ(hằngTên, "getLength") && vănBảnTừ(hằngBộMôTả, "()I") || vănBảnTừ(hằngTên, "getAddress") && vănBảnTừ(hằngBộMôTả, "()Ljava/net/InetAddress;") || vănBảnTừ(hằngTên, "getPort") && vănBảnTừ(hằngBộMôTả, "()I"))) {
                int thamChiếuĐốiTượng = trừCácGiáTrị(2); if (!giáTrịĐốiTượng(thamChiếuĐốiTượng, 16)) return;
                int vịTríMục = vănBảnTừ(hằngTên, "getData") ? 2 : vănBảnTừ(hằngTên, "getLength") ? 3 : vănBảnTừ(hằngTên, "getAddress") ? 4 : 5;
                đặtGiáTrị(giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + vịTríMục], vịTríMục == 2 || vịTríMục == 4 ? 2 : 1); return;
            }
        }
        if (vănBảnTừ(chủSởHữu, "java/net/DatagramSocket")) {
            if (mãLệnh == 183 && vănBảnTừ(hằngTên, "<init>") && (vănBảnTừ(hằngBộMôTả, "()V") || vănBảnTừ(hằngBộMôTả, "(I)V"))) {
                int sốCổng = vănBảnTừ(hằngBộMôTả, "()V") ? 0 : trừCácGiáTrị(1), thamChiếuĐốiTượng = trừCácGiáTrị(2); if (!giáTrịĐốiTượng(thamChiếuĐốiTượng, 15)) return;
                if (sốCổng < 0 || sốCổng > 65535) { némNgoạiLệ(9, "invalid port"); return; }
                int sốTệpĐãMở = NgườiDùng.mởMạng(sốCổng); if (sốTệpĐãMở < 0) némNgoạiLệ(39, "UDP socket/bind failed"); else giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2] = sốTệpĐãMở; return;
            }
            if (mãLệnh == 182 && vănBảnTừ(hằngTên, "setSoTimeout") && vănBảnTừ(hằngBộMôTả, "(I)V")) {
                int giáTrịMiliGiây = trừCácGiáTrị(1), thamChiếuĐốiTượng = trừCácGiáTrị(2); if (!giáTrịĐốiTượng(thamChiếuĐốiTượng, 15)) return;
                if (giáTrịMiliGiây < 0) némNgoạiLệ(9, "negative timeout"); else giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 3] = giáTrịMiliGiây; return;
            }
            if (mãLệnh == 182 && vănBảnTừ(hằngTên, "getLocalPort") && vănBảnTừ(hằngBộMôTả, "()I")) { int thamChiếuĐốiTượng = trừCácGiáTrị(2); if (giáTrịĐốiTượng(thamChiếuĐốiTượng, 15)) đặtGiáTrị(giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2] < 0 ? -1 : NgườiDùng.cổngMạng(giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2]), 1); return; }
            if (mãLệnh == 182 && vănBảnTừ(hằngTên, "isClosed") && vănBảnTừ(hằngBộMôTả, "()Z")) { int thamChiếuĐốiTượng = trừCácGiáTrị(2); if (giáTrịĐốiTượng(thamChiếuĐốiTượng, 15)) đặtGiáTrị(giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2] < 0 ? 1 : 0, 1); return; }
            if (mãLệnh == 182 && vănBảnTừ(hằngTên, "close") && vănBảnTừ(hằngBộMôTả, "()V")) { int thamChiếuĐốiTượng = trừCácGiáTrị(2); if (giáTrịĐốiTượng(thamChiếuĐốiTượng, 15) && giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2] >= 0) { NgườiDùng.đóngBộMôTảTệp(giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2]); giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2] = -1; } return; }
            if (mãLệnh == 182 && (vănBảnTừ(hằngTên, "send") || vănBảnTừ(hằngTên, "receive")) && vănBảnTừ(hằngBộMôTả, "(Ljava/net/DatagramPacket;)V")) {
                int góiTin = trừCácGiáTrị(2), thamChiếuĐốiTượng = trừCácGiáTrị(2); if (!giáTrịĐốiTượng(góiTin, 16) || !giáTrịĐốiTượng(thamChiếuĐốiTượng, 15)) return;
                int mảngDữLiệu = giáTrịVùngNhớĐộng[góiTin + 2], độDàiHợpLệ = giáTrịVùngNhớĐộng[góiTin + 3], sốTệpĐãMở = giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2];
                if (sốTệpĐãMở < 0) { némNgoạiLệ(39, "socket closed"); return; }
                if (vănBảnTừ(hằngTên, "send")) {
                    if (!giáTrịĐốiTượng(giáTrịVùngNhớĐộng[góiTin + 4], 14)) return;
                    if (độDàiHợpLệ > 512) { némNgoạiLệ(11, "datagram limit (512 bytes)"); return; }
                    for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < độDàiHợpLệ; chỉSốVòngLặp++) giáTrịTạmMạng[chỉSốVòngLặp] = giáTrịVùngNhớĐộng[mảngDữLiệu + 2 + chỉSốVòngLặp];
                    if (NgườiDùng.gửiMạng(sốTệpĐãMở, giáTrịVùngNhớĐộng[giáTrịVùngNhớĐộng[góiTin + 4] + 2], giáTrịVùngNhớĐộng[góiTin + 5], giáTrịTạmMạng, độDàiHợpLệ) < 0) némNgoạiLệ(11, "UDP send failed");
                } else {
                    int sốLượngMục = NgườiDùng.nhậnMạng(sốTệpĐãMở, giáTrịTạmMạng, độDàiHợpLệ > 512 ? 512 : độDàiHợpLệ);
                    if (sốLượngMục == -11) {
                        int thờiGianHiệnTại = NgườiDùng.miliGiây();
                        if (giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 4] == 0) giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 4] = thờiGianHiệnTại + 1;
                        if (giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 3] > 0 && thờiGianHiệnTại - (giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 4] - 1) >= giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 3]) { giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 4] = 0; némNgoạiLệ(19, "receive timed out"); return; }
                        đặtGiáTrị(thamChiếuĐốiTượng, 2); đặtGiáTrị(góiTin, 2); vịTríKhung[chỉSốKhung] = chỉLệnhKhung[chỉSốKhung]; đổiYêuCầu = true; return;
                    }
                    giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 4] = 0;
                    if (sốLượngMục < 0) { némNgoạiLệ(11, "UDP receive failed"); return; }
                    for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < sốLượngMục; chỉSốVòngLặp++) giáTrịVùngNhớĐộng[mảngDữLiệu + 2 + chỉSốVòngLặp] = (byte)giáTrịTạmMạng[chỉSốVòngLặp];
                    giáTrịVùngNhớĐộng[góiTin + 3] = sốLượngMục; giáTrịVùngNhớĐộng[góiTin + 4] = đốiTượngĐịaChỉ(giáTrịTạmMạng[513]); thamChiếuVùngNhớĐộng[góiTin + 4] = 1; giáTrịVùngNhớĐộng[góiTin + 5] = giáTrịTạmMạng[512];
                }
                return;
            }
        }
        giáTrịSựThấtBại("unsupported java.net method");
    }
    static boolean chờLuồngCho(int thamChiếuĐốiTượng) {
        int thờiGianHiệnTại = NgườiDùng.miliGiây();
        if (giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 5] == 0) giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 5] = thờiGianHiệnTại + 1;
        if (giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 3] > 0 && thờiGianHiệnTại - (giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 5] - 1) >= giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 3]) { giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 5] = 0; némNgoạiLệ(19, "stream wait timed out"); return false; }
        vịTríKhung[chỉSốKhung] = chỉLệnhKhung[chỉSốKhung]; đổiYêuCầu = true; return true;
    }
    static void gọiThựcHiệnLuồng(int chủSởHữu, int hằngTên, int hằngBộMôTả, int mãLệnh) {
        boolean nhậnTrang = vănBảnTừ(chủSởHữu, "java/net/ServerSocket"), luồng = vănBảnTừ(chủSởHữu, "java/io/InputStream") || vănBảnTừ(chủSởHữu, "java/io/OutputStream");
        if (!luồng && mãLệnh == 183 && vănBảnTừ(hằngTên, "<init>")) {
            boolean làTrạngTháiRỗng = vănBảnTừ(hằngBộMôTả, "()V"), đượcĐặtTên = vănBảnTừ(hằngBộMôTả, "(Ljava/lang/String;I)V"), đượcĐịnhĐịaChỉ = vănBảnTừ(hằngBộMôTả, "(Ljava/net/InetAddress;I)V");
            if (!(làTrạngTháiRỗng || nhậnTrang && vănBảnTừ(hằngBộMôTả, "(I)V") || !nhậnTrang && (đượcĐặtTên || đượcĐịnhĐịaChỉ))) { giáTrịSựThấtBại("unsupported socket constructor"); return; }
            int sốCổng = làTrạngTháiRỗng ? 0 : trừCácGiáTrị(1), thamChiếuĐịaChỉ = đượcĐặtTên || đượcĐịnhĐịaChỉ ? trừCácGiáTrị(2) : 0, thamChiếuĐốiTượng = trừCácGiáTrị(2);
            if (!giáTrịĐốiTượng(thamChiếuĐốiTượng, nhậnTrang ? 18 : 17)) return;
            if (sốCổng < 0 || sốCổng > 65535) { némNgoạiLệ(9, "invalid port"); return; }
            if (đượcĐịnhĐịaChỉ && !giáTrịĐốiTượng(thamChiếuĐịaChỉ, 14)) return;
            int địaChỉMạng = đượcĐặtTên ? giảiMãĐịaChỉ(thamChiếuĐịaChỉ) : đượcĐịnhĐịaChỉ ? giáTrịVùngNhớĐộng[thamChiếuĐịaChỉ + 2] : 0x7f000001;
            if (lỗi || đốiTượngĐãNém != 0) return;
            int sốTệpĐãMở = NgườiDùng.điềuKhiểnLuồng(0, 0, 0); if (sốTệpĐãMở < 0) { némNgoạiLệ(39, "socket slots exhausted"); return; }
            int giáTrịĐãXửLý = làTrạngTháiRỗng ? 0 : nhậnTrang ? NgườiDùng.điềuKhiểnLuồng(1, sốTệpĐãMở, sốCổng) : NgườiDùng.kếtNốiLuồng(sốTệpĐãMở, địaChỉMạng, sốCổng);
            if (giáTrịĐãXửLý < 0) { NgườiDùng.đóngBộMôTảTệp(sốTệpĐãMở); némNgoạiLệ(39, "socket bind/connect failed"); return; }
            giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2] = sốTệpĐãMở; giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 4] = sốCổng; giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 6] = làTrạngTháiRỗng ? 0 : 1; return;
        }
        if (!luồng && vănBảnTừ(hằngTên, "setSoTimeout") && vănBảnTừ(hằngBộMôTả, "(I)V")) { int giáTrịMiliGiây = trừCácGiáTrị(1), thamChiếuĐốiTượng = trừCácGiáTrị(2); if (!giáTrịĐốiTượng(thamChiếuĐốiTượng, nhậnTrang ? 18 : 17)) return; if (giáTrịMiliGiây < 0) némNgoạiLệ(9, "negative timeout"); else giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 3] = giáTrịMiliGiây; return; }
        if (!luồng && vănBảnTừ(hằngTên, "close") && vănBảnTừ(hằngBộMôTả, "()V")) { int thamChiếuĐốiTượng = trừCácGiáTrị(2); if (giáTrịĐốiTượng(thamChiếuĐốiTượng, nhậnTrang ? 18 : 17) && giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2] >= 0) { NgườiDùng.đóngBộMôTảTệp(giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2]); giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2] = -1; } return; }
        if (!luồng && (vănBảnTừ(hằngTên, "getLocalPort") || vănBảnTừ(hằngTên, "getPort") || vănBảnTừ(hằngTên, "isClosed") || vănBảnTừ(hằngTên, "isConnected"))) {
            int thamChiếuĐốiTượng = trừCácGiáTrị(2); if (!giáTrịĐốiTượng(thamChiếuĐốiTượng, nhậnTrang ? 18 : 17)) return;
            đặtGiáTrị(vănBảnTừ(hằngTên, "isClosed") ? giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2] < 0 ? 1 : 0 : vănBảnTừ(hằngTên, "isConnected") ? giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 6] : vănBảnTừ(hằngTên, "getPort") ? giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 4] : giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2] < 0 ? -1 : NgườiDùng.điềuKhiểnLuồng(4, giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2], 0), 1); return;
        }
        if (nhậnTrang && vănBảnTừ(hằngTên, "accept") && vănBảnTừ(hằngBộMôTả, "()Ljava/net/Socket;")) {
            int thamChiếuĐốiTượng = trừCácGiáTrị(2); if (!giáTrịĐốiTượng(thamChiếuĐốiTượng, 18)) return; int sốTệpĐãMở = NgườiDùng.điềuKhiểnLuồng(3, giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2], 0);
            if (sốTệpĐãMở == -11) { if (chờLuồngCho(thamChiếuĐốiTượng)) đặtGiáTrị(thamChiếuĐốiTượng, 2); return; }
            giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 5] = 0; if (sốTệpĐãMở < 0) { némNgoạiLệ(11, "accept failed"); return; }
            int giáTrịĐãTrảVề = cấpPhátLưuTrữ(17, 5); if (lỗi) { NgườiDùng.đóngBộMôTảTệp(sốTệpĐãMở); return; } giáTrịVùngNhớĐộng[giáTrịĐãTrảVề + 2] = sốTệpĐãMở; giáTrịVùngNhớĐộng[giáTrịĐãTrảVề + 4] = NgườiDùng.điềuKhiểnLuồng(5, sốTệpĐãMở, 0); giáTrịVùngNhớĐộng[giáTrịĐãTrảVề + 6] = 1; đặtGiáTrị(giáTrịĐãTrảVề, 2); return;
        }
        if (!nhậnTrang && !luồng && ((vănBảnTừ(hằngTên, "getInputStream") && vănBảnTừ(hằngBộMôTả, "()Ljava/io/InputStream;")) || (vănBảnTừ(hằngTên, "getOutputStream") && vănBảnTừ(hằngBộMôTả, "()Ljava/io/OutputStream;")))) {
            int thamChiếuĐốiTượng = trừCácGiáTrị(2); if (!giáTrịĐốiTượng(thamChiếuĐốiTượng, 17)) return; if (giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2] < 0 || giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 6] == 0) { némNgoạiLệ(39, "socket is not connected"); return; }
            int giáTrịĐãTrảVề = cấpPhátLưuTrữ(19, 4); if (lỗi) return; giáTrịVùngNhớĐộng[giáTrịĐãTrảVề + 2] = thamChiếuĐốiTượng; thamChiếuVùngNhớĐộng[giáTrịĐãTrảVề + 2] = 1; giáTrịVùngNhớĐộng[giáTrịĐãTrảVề + 3] = vănBảnTừ(hằngTên, "getInputStream") ? 0 : 1; đặtGiáTrị(giáTrịĐãTrảVề, 2); return;
        }
        if (luồng) {
            boolean cóĐọc = vănBảnTừ(hằngTên, "read"), làThaoTácGhi = vănBảnTừ(hằngTên, "write"), khối = vănBảnTừ(hằngBộMôTả, "([B)I") || vănBảnTừ(hằngBộMôTả, "([B)V"), làMảngCon = vănBảnTừ(hằngBộMôTả, "([BII)I") || vănBảnTừ(hằngBộMôTả, "([BII)V");
            int sốLượngMục = làMảngCon ? trừCácGiáTrị(1) : 0, bắtChạyĐộDời = làMảngCon ? trừCácGiáTrị(1) : 0, mảngDữLiệu = khối || làMảngCon ? trừCácGiáTrị(2) : 0;
            int giáTrịDữLiệu = làThaoTácGhi && vănBảnTừ(hằngBộMôTả, "(I)V") ? trừCácGiáTrị(1) : 0, thamChiếuĐốiTượng = trừCácGiáTrị(2);
            if (!giáTrịĐốiTượng(thamChiếuĐốiTượng, 19)) return; int thamChiếuCha = giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2], sốTệpĐãMở = giáTrịVùngNhớĐộng[thamChiếuCha + 2];
            if (sốTệpĐãMở < 0) { némNgoạiLệ(11, "stream closed"); return; }
            if (vănBảnTừ(hằngTên, "close") && vănBảnTừ(hằngBộMôTả, "()V")) { NgườiDùng.đóngBộMôTảTệp(sốTệpĐãMở); giáTrịVùngNhớĐộng[thamChiếuCha + 2] = -1; return; }
            if (vănBảnTừ(hằngTên, "flush") && vănBảnTừ(hằngBộMôTả, "()V")) return;
            if ((!cóĐọc && !làThaoTácGhi) || cóĐọc != (giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 3] == 0)) { giáTrịSựThấtBại("unsupported stream operation"); return; }
            if (khối || làMảngCon) { if (!giáTrịĐốiTượng(mảngDữLiệu, 20)) return; if (khối) sốLượngMục = giáTrịVùngNhớĐộng[mảngDữLiệu + 1]; if (bắtChạyĐộDời < 0 || sốLượngMục < 0 || bắtChạyĐộDời > giáTrịVùngNhớĐộng[mảngDữLiệu + 1] - sốLượngMục) { némNgoạiLệ(6, "stream array bounds"); return; } }
            else sốLượngMục = 1;
            if (sốLượngMục == 0) { if (cóĐọc) đặtGiáTrị(0, 1); return; }
            int sốLượngĐãHoànTất = làThaoTácGhi ? giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 4] : 0, giáTrịĐãXửLý = 0;
            while (sốLượngĐãHoànTất < sốLượngMục) {
                giáTrịĐãXửLý = cóĐọc ? NgườiDùng.đọcByteTệpMột(sốTệpĐãMở) : NgườiDùng.ghiByteTệpMột(sốTệpĐãMở, khối || làMảngCon ? giáTrịVùngNhớĐộng[mảngDữLiệu + 2 + bắtChạyĐộDời + sốLượngĐãHoànTất] : giáTrịDữLiệu);
                if (giáTrịĐãXửLý < 0 || cóĐọc && giáTrịĐãXửLý == 256) break;
                if (cóĐọc && (khối || làMảngCon)) giáTrịVùngNhớĐộng[mảngDữLiệu + 2 + bắtChạyĐộDời + sốLượngĐãHoànTất] = (byte)giáTrịĐãXửLý;
                sốLượngĐãHoànTất++; if (cóĐọc && !(khối || làMảngCon)) break;
            }
            if (giáTrịĐãXửLý == -11 && (làThaoTácGhi || sốLượngĐãHoànTất == 0)) {
                giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 4] = sốLượngĐãHoànTất;
                if (chờLuồngCho(thamChiếuCha)) { đặtGiáTrị(thamChiếuĐốiTượng, 2); if (khối || làMảngCon) đặtGiáTrị(mảngDữLiệu, 2); if (làMảngCon) { đặtGiáTrị(bắtChạyĐộDời, 1); đặtGiáTrị(sốLượngMục, 1); } if (làThaoTácGhi && !(khối || làMảngCon)) đặtGiáTrị(giáTrịDữLiệu, 1); } return;
            }
            giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 4] = 0; giáTrịVùngNhớĐộng[thamChiếuCha + 5] = 0;
            if (giáTrịĐãXửLý < 0 && giáTrịĐãXửLý != -11) { némNgoạiLệ(11, "stream I/O failed"); return; }
            if (cóĐọc) đặtGiáTrị(sốLượngĐãHoànTất == 0 && giáTrịĐãXửLý == 256 ? -1 : khối || làMảngCon ? sốLượngĐãHoànTất : giáTrịĐãXửLý, 1); return;
        }
        giáTrịSựThấtBại("unsupported Socket/ServerSocket method");
    }
    static int[] thamChiếuMànHình = new int[32], vănBảnMànHìnhTạm = new int[256], vềSauLậpLịch = new int[8];
    static int sốLượngVềSau;
    static int[] giáTrịTiếngHànVềSau = new int[8];
    static boolean làSựKiệnViệcXửLý;
    static int lớpMànHìnhTiếngHàn(int hằngTên) {
        if (vănBảnTừ(hằngTên, "tiếngViệt/tựThân/cửaSổ")) return 24;
        if (vănBảnTừ(hằngTên, "tiếngViệt/tựThân/nhãn")) return 26;
        if (vănBảnTừ(hằngTên, "tiếngViệt/tựThân/nút")) return 27;
        if (vănBảnTừ(hằngTên, "tiếngViệt/tựThân/TrườngVănBản")) return 28;
        if (vănBảnTừ(hằngTên, "tiếngViệt/tựThân/ThôngBáoHànhĐộng")) return 29;
        return 0;
    }
    static boolean chủSởHữuMànHìnhTiếngHàn(int hằngTên) {
        return lớpMànHìnhTiếngHàn(hằngTên) != 0 || vănBảnTừ(hằngTên, "tiếngViệt/tựThân/PhầnTửMànHình") || vănBảnTừ(hằngTên, "tiếngViệt/tựThân/HàngĐợiSựKiện");
    }
    static int lớpMànHình(int hằngTên) {
        int LớpTiếngHàn = lớpMànHìnhTiếngHàn(hằngTên); if (LớpTiếngHàn != 0) return LớpTiếngHàn;
        if (vănBảnTừ(hằngTên, "javax/swing/JFrame")) return 24;
        if (vănBảnTừ(hằngTên, "javax/swing/JPanel")) return 25;
        if (vănBảnTừ(hằngTên, "javax/swing/JLabel")) return 26;
        if (vănBảnTừ(hằngTên, "javax/swing/JButton")) return 27;
        if (vănBảnTừ(hằngTên, "javax/swing/JTextField")) return 28;
        if (vănBảnTừ(hằngTên, "java/awt/event/ActionEvent")) return 29;
        if (vănBảnTừ(hằngTên, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean chủSởHữuMànHình(int hằngTên) {
        return lớpMànHình(hằngTên) != 0 || vănBảnTừ(hằngTên, "java/awt/Component") || vănBảnTừ(hằngTên, "java/awt/Container") || vănBảnTừ(hằngTên, "javax/swing/JComponent") || vănBảnTừ(hằngTên, "javax/swing/AbstractButton") || vănBảnTừ(hằngTên, "javax/swing/text/JTextComponent") || vănBảnTừ(hằngTên, "javax/swing/SwingUtilities");
    }
    static boolean đốiTượngMànHình(int thamChiếuĐốiTượng) { if (!làĐốiTượngHợpLệ(thamChiếuĐốiTượng)) return false; if (giáTrịVùngNhớĐộng[thamChiếuĐốiTượng] < 24 || giáTrịVùngNhớĐộng[thamChiếuĐốiTượng] > 28) { giáTrịSựThấtBại("unsupported Swing receiver"); return false; } return true; }
    static void đặtGiáTrịKýTựMànHình(int thamChiếuĐốiTượng, int thamChiếuVănBản) {
        if (thamChiếuVănBản != 0 && !giáTrịĐốiTượng(thamChiếuVănBản, 1)) return;
        int sốLượngMục = thamChiếuVănBản == 0 ? 0 : giáTrịVùngNhớĐộng[thamChiếuVănBản + 1]; if (sốLượngMục > 254) { némNgoạiLệ(9, "GUI text limit"); return; }
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < sốLượngMục; chỉSốVòngLặp++) vănBảnMànHìnhTạm[chỉSốVòngLặp] = giáTrịVùngNhớĐộng[thamChiếuVănBản + 2 + chỉSốVòngLặp];
        if (NgườiDùng.vănBảnMànHình(giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2], vănBảnMànHìnhTạm, sốLượngMục) < 0) { némNgoạiLệ(9, "GUI text too long/invalid"); return; }
        giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 3] = thamChiếuVănBản; thamChiếuVùngNhớĐộng[thamChiếuĐốiTượng + 3] = 1;
    }
    static int đọcKýTựMànHình(int thamChiếuĐốiTượng) {
        int giáTrịCănCước = giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2], sốLượngMục = NgườiDùng.kếtNốiMànHình(8, giáTrịCănCước, 0, 0, 0, 0), sốLượngĐãDùng = 0;
        if (sốLượngMục < 0) { giáTrịSựThấtBại("GUI text read failed"); return 0; }
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < sốLượngMục; chỉSốVòngLặp++) { int giáTrịĐãMãHóa = NgườiDùng.kếtNốiMànHình(9, giáTrịCănCước, chỉSốVòngLặp, 0, 0, 0); if (giáTrịĐãMãHóa >= 65536) { giáTrịĐãMãHóa -= 65536; vănBảnMànHìnhTạm[sốLượngĐãDùng++] = 0xd800 | giáTrịĐãMãHóa >> 10; vănBảnMànHìnhTạm[sốLượngĐãDùng++] = 0xdc00 | giáTrịĐãMãHóa & 1023; } else vănBảnMànHìnhTạm[sốLượngĐãDùng++] = giáTrịĐãMãHóa; }
        int giáTrịĐãTrảVề = cấpPhátLưuTrữ(1, sốLượngĐãDùng); if (!lỗi) for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < sốLượngĐãDùng; chỉSốVòngLặp++) giáTrịVùngNhớĐộng[giáTrịĐãTrảVề + 2 + chỉSốVòngLặp] = vănBảnMànHìnhTạm[chỉSốVòngLặp]; return giáTrịĐãTrảVề;
    }
    /* Tạo trực tiếp đối tượng của API tiếng Việt rồi nối với chức năng đồ họa của nhân; không tạo đối tượng hay bộ chuyển tiếp Swing. */
    static void gọiThựcHiệnMànHìnhTiếngHàn(int chủSởHữu, int hằngTên, int hằngBộMôTả, int mãLệnh) {
        if (vănBảnTừ(chủSởHữu, "tiếngViệt/tựThân/HàngĐợiSựKiện")) {
            if (mãLệnh == 184 && vănBảnTừ(hằngTên, "gọiThựcHiệnVềSau") && vănBảnTừ(hằngBộMôTả, "(LtiếngViệt/tựThân/TácVụChạyĐược;)V")) {
                int HànhĐộngTácVụ = trừCácGiáTrị(2); if (!làĐốiTượngHợpLệ(HànhĐộngTácVụ)) return;
                if (sốLượngVềSau == 8) { giáTrịSựThấtBại("MànHình TácVụ 대기열이 가득 찼습니다"); return; }
                giáTrịTiếngHànVềSau[sốLượngVềSau] = 1; vềSauLậpLịch[sốLượngVềSau++] = HànhĐộngTácVụ; return;
            }
            if (mãLệnh == 184 && vănBảnTừ(hằngTên, "làĐangĐiềuPhốiSựKiện") && vănBảnTừ(hằngBộMôTả, "()Z")) { đặtGiáTrị(làSựKiệnViệcXửLý ? 1 : 0, 1); return; }
            giáTrịSựThấtBại("지원하지 않는 tiếngViệt MànHình 일정 gọiThựcHiện"); return;
        }
        if (vănBảnTừ(chủSởHữu, "tiếngViệt/tựThân/ThôngBáoHànhĐộng")) {
            int thôngBáo = trừCácGiáTrị(2); if (!giáTrịĐốiTượng(thôngBáo, 29) || giáTrịVùngNhớĐộng[thôngBáo + 3] == 0) return;
            if (vănBảnTừ(hằngTên, "nguồnSựKiện") && vănBảnTừ(hằngBộMôTả, "()LtiếngViệt/tựThân/PhầnTửMànHình;")) đặtGiáTrị(giáTrịVùngNhớĐộng[thôngBáo + 2], 2);
            else if (vănBảnTừ(hằngTên, "vănBảnLệnh") && vănBảnTừ(hằngBộMôTả, "()Ljava/lang/String;")) đặtGiáTrị(đọcKýTựMànHình(giáTrịVùngNhớĐộng[thôngBáo + 2]), 2);
            else if (vănBảnTừ(hằngTên, "sốHiệu") && vănBảnTừ(hằngBộMôTả, "()I")) đặtGiáTrị(1001, 1);
            else giáTrịSựThấtBại("지원하지 않는 tiếngViệt hànhĐộng thôngBáo gọiThựcHiện"); return;
        }
        if (mãLệnh == 183 && vănBảnTừ(hằngTên, "<init>")) {
            int giáTrịLoại = lớpMànHìnhTiếngHàn(chủSởHữu), giáTrịBộNhận = 0, vịTríNgang = 0, vịTríDọc = 0, khoảngTrảiRộng = 0, giáTrịCao = 0;
            if (giáTrịLoại == 24 && vănBảnTừ(hằngBộMôTả, "(Ljava/lang/String;II)V")) {
                giáTrịCao = trừCácGiáTrị(1); khoảngTrảiRộng = trừCácGiáTrị(1); vịTríNgang = (NgườiDùng.rộngMànHình() - khoảngTrảiRộng) / 2; vịTríDọc = (NgườiDùng.caoMànHình() - giáTrịCao) / 2;
            } else if ((giáTrịLoại == 26 || giáTrịLoại == 28) && vănBảnTừ(hằngBộMôTả, "(Ljava/lang/String;IIII)V") || giáTrịLoại == 27 && vănBảnTừ(hằngBộMôTả, "(Ljava/lang/String;IIIILtiếngViệt/tựThân/BộNhậnHànhĐộng;)V")) {
                if (giáTrịLoại == 27) giáTrịBộNhận = trừCácGiáTrị(2);
                giáTrịCao = trừCácGiáTrị(1); khoảngTrảiRộng = trừCácGiáTrị(1); vịTríDọc = trừCácGiáTrị(1); vịTríNgang = trừCácGiáTrị(1);
            } else { giáTrịSựThấtBại("지원하지 않는 tiếngViệt MànHình 생성자"); return; }
            int vănBản = trừCácGiáTrị(2), giáTrịPhầnTử = trừCácGiáTrị(2); if (!đốiTượngMànHình(giáTrịPhầnTử)) return;
            if (khoảngTrảiRộng < 1 || giáTrịCao < 1 || vịTríNgang < 0 || vịTríDọc < 0 || khoảngTrảiRộng > NgườiDùng.rộngMànHình() - vịTríNgang || giáTrịCao > NgườiDùng.caoMànHình() - vịTríDọc) { némNgoạiLệ(27, "MànHình 영역을 벗어난 크기입니다"); return; }
            int sốHiệu = NgườiDùng.kếtNốiMànHình(0, giáTrịLoại - 23, 0, 0, 0, 0);
            if (sốHiệu < 1 || sốHiệu > 32) { giáTrịSựThấtBại("MànHình giáTrịPhầnTử 자리가 가득 찼습니다"); return; }
            giáTrịVùngNhớĐộng[giáTrịPhầnTử + 2] = sốHiệu; thamChiếuMànHình[sốHiệu - 1] = giáTrịPhầnTử;
            giáTrịVùngNhớĐộng[giáTrịPhầnTử + 5] = vịTríNgang; giáTrịVùngNhớĐộng[giáTrịPhầnTử + 6] = vịTríDọc; giáTrịVùngNhớĐộng[giáTrịPhầnTử + 7] = khoảngTrảiRộng; giáTrịVùngNhớĐộng[giáTrịPhầnTử + 8] = giáTrịCao; giáTrịVùngNhớĐộng[giáTrịPhầnTử + 10] = 2;
            giáTrịVùngNhớĐộng[giáTrịPhầnTử + 4] = giáTrịBộNhận; thamChiếuVùngNhớĐộng[giáTrịPhầnTử + 4] = 1; giáTrịVùngNhớĐộng[giáTrịPhầnTử + 12] = 1;
            NgườiDùng.kếtNốiMànHình(1, sốHiệu, vịTríNgang, vịTríDọc, khoảngTrảiRộng, giáTrịCao);
            if (giáTrịLoại == 24) NgườiDùng.kếtNốiMànHình(7, sốHiệu, 2, 0, 0, 0);
            đặtGiáTrịKýTựMànHình(giáTrịPhầnTử, vănBản); return;
        }
        if (mãLệnh != 182) { giáTrịSựThấtBại("잘못된 tiếngViệt MànHình gọiThựcHiện lệnh"); return; }
        if (vănBảnTừ(hằngTên, "ghiVănBản") && vănBảnTừ(hằngBộMôTả, "(Ljava/lang/String;)V")) {
            int vănBản = trừCácGiáTrị(2), giáTrịPhầnTử = trừCácGiáTrị(2); if (đốiTượngMànHình(giáTrịPhầnTử)) đặtGiáTrịKýTựMànHình(giáTrịPhầnTử, vănBản); return;
        }
        if (vănBảnTừ(hằngTên, "đọcVănBản") && vănBảnTừ(hằngBộMôTả, "()Ljava/lang/String;")) {
            int giáTrịPhầnTử = trừCácGiáTrị(2); if (đốiTượngMànHình(giáTrịPhầnTử)) đặtGiáTrị(đọcKýTựMànHình(giáTrịPhầnTử), 2); return;
        }
        if (vănBảnTừ(hằngTên, "đặtGiáTrịBộNhậnHànhĐộng") && vănBảnTừ(hằngBộMôTả, "(LtiếngViệt/tựThân/BộNhậnHànhĐộng;)V")) {
            int giáTrịBộNhận = trừCácGiáTrị(2), giáTrịPhầnTử = trừCácGiáTrị(2);
            if (đốiTượngMànHình(giáTrịPhầnTử)) { giáTrịVùngNhớĐộng[giáTrịPhầnTử + 4] = giáTrịBộNhận; thamChiếuVùngNhớĐộng[giáTrịPhầnTử + 4] = 1; giáTrịVùngNhớĐộng[giáTrịPhầnTử + 12] = 1; } return;
        }
        if (vănBảnTừ(hằngTên, "thêmPhầnTử") && vănBảnTừ(hằngBộMôTả, "(LtiếngViệt/tựThân/PhầnTửMànHình;)V")) {
            int giáTrịCon = trừCácGiáTrị(2), giáTrịCha = trừCácGiáTrị(2); if (!đốiTượngMànHình(giáTrịCon) || !đốiTượngMànHình(giáTrịCha)) return;
            if (NgườiDùng.kếtNốiMànHình(2, giáTrịVùngNhớĐộng[giáTrịCha + 2], giáTrịVùngNhớĐộng[giáTrịCon + 2], 0, 0, 0) < 0) { némNgoạiLệ(27, "잘못된 MànHình 부모입니다"); return; }
            giáTrịVùngNhớĐộng[giáTrịCon + 11] = giáTrịCha; thamChiếuVùngNhớĐộng[giáTrịCon + 11] = 1; return;
        }
        if (vănBảnTừ(hằngTên, "đặtGiáTrịCácCận") && vănBảnTừ(hằngBộMôTả, "(IIII)V")) {
            int giáTrịCao = trừCácGiáTrị(1), khoảngTrảiRộng = trừCácGiáTrị(1), vịTríDọc = trừCácGiáTrị(1), vịTríNgang = trừCácGiáTrị(1), giáTrịPhầnTử = trừCácGiáTrị(2); if (!đốiTượngMànHình(giáTrịPhầnTử)) return;
            if (NgườiDùng.kếtNốiMànHình(1, giáTrịVùngNhớĐộng[giáTrịPhầnTử + 2], vịTríNgang, vịTríDọc, khoảngTrảiRộng, giáTrịCao) < 0) { némNgoạiLệ(27, "MànHình 영역을 벗어난 자리입니다"); return; }
            giáTrịVùngNhớĐộng[giáTrịPhầnTử + 5] = vịTríNgang; giáTrịVùngNhớĐộng[giáTrịPhầnTử + 6] = vịTríDọc; giáTrịVùngNhớĐộng[giáTrịPhầnTử + 7] = khoảngTrảiRộng; giáTrịVùngNhớĐộng[giáTrịPhầnTử + 8] = giáTrịCao; return;
        }
        if ((vănBảnTừ(hằngTên, "hiệnCửaSổ") || vănBảnTừ(hằngTên, "đóng")) && vănBảnTừ(hằngBộMôTả, "()V")) {
            boolean giáTrịTínhHiểnThị = vănBảnTừ(hằngTên, "hiệnCửaSổ"); int giáTrịPhầnTử = trừCácGiáTrị(2); if (!đốiTượngMànHình(giáTrịPhầnTử)) return;
            if (NgườiDùng.kếtNốiMànHình(giáTrịTínhHiểnThị ? 3 : 4, giáTrịVùngNhớĐộng[giáTrịPhầnTử + 2], giáTrịTínhHiểnThị ? 1 : 0, 0, 0, 0) < 0) { giáTrịSựThấtBại("화면은 tươngTác 명령에서 실행해야 합니다"); return; }
            giáTrịVùngNhớĐộng[giáTrịPhầnTử + 9] = giáTrịTínhHiểnThị ? 1 : 0; return;
        }
        if (vănBảnTừ(hằngTên, "làHiệnĐược") && vănBảnTừ(hằngBộMôTả, "()Z")) { int giáTrịPhầnTử = trừCácGiáTrị(2); if (đốiTượngMànHình(giáTrịPhầnTử)) đặtGiáTrị(giáTrịVùngNhớĐộng[giáTrịPhầnTử + 9], 1); return; }
        giáTrịSựThấtBại("지원하지 않는 tiếngViệt MànHình giáTrịPhươngThức");
    }
    static void gọiThựcHiệnMànHình(int chủSởHữu, int hằngTên, int hằngBộMôTả, int mãLệnh) {
        if (vănBảnTừ(chủSởHữu, "javax/swing/SwingUtilities")) {
            if (mãLệnh == 184 && vănBảnTừ(hằngTên, "invokeLater") && vănBảnTừ(hằngBộMôTả, "(Ljava/lang/Runnable;)V")) { int thamChiếuĐốiTượng = trừCácGiáTrị(2); if (!làĐốiTượngHợpLệ(thamChiếuĐốiTượng)) return; if (sốLượngVềSau == 8) { giáTrịSựThấtBại("invokeLater queue full"); return; } vềSauLậpLịch[sốLượngVềSau++] = thamChiếuĐốiTượng; return; }
            if (mãLệnh == 184 && vănBảnTừ(hằngTên, "isEventDispatchThread") && vănBảnTừ(hằngBộMôTả, "()Z")) { đặtGiáTrị(làSựKiệnViệcXửLý ? 1 : 0, 1); return; }
            giáTrịSựThấtBại("unsupported SwingUtilities method"); return;
        }
        if (vănBảnTừ(chủSởHữu, "java/awt/event/ActionEvent")) {
            int thamChiếuĐốiTượng = trừCácGiáTrị(2); if (!giáTrịĐốiTượng(thamChiếuĐốiTượng, 29)) return;
            if (vănBảnTừ(hằngTên, "getSource") && vănBảnTừ(hằngBộMôTả, "()Ljava/lang/Object;")) đặtGiáTrị(giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2], 2);
            else if (vănBảnTừ(hằngTên, "getActionCommand") && vănBảnTừ(hằngBộMôTả, "()Ljava/lang/String;")) đặtGiáTrị(đọcKýTựMànHình(giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2]), 2);
            else if (vănBảnTừ(hằngTên, "getID") && vănBảnTừ(hằngBộMôTả, "()I")) đặtGiáTrị(1001, 1);
            else giáTrịSựThấtBại("unsupported ActionEvent method"); return;
        }
        if (mãLệnh == 183 && vănBảnTừ(hằngTên, "<init>")) {
            int cácCột = 0, thamChiếuVănBản = 0;
            if (vănBảnTừ(hằngBộMôTả, "(I)V")) cácCột = trừCácGiáTrị(1);
            else if (vănBảnTừ(hằngBộMôTả, "(Ljava/lang/String;I)V")) { cácCột = trừCácGiáTrị(1); thamChiếuVănBản = trừCácGiáTrị(2); }
            else if (vănBảnTừ(hằngBộMôTả, "(Ljava/lang/String;)V")) thamChiếuVănBản = trừCácGiáTrị(2);
            else if (vănBảnTừ(hằngBộMôTả, "(Ljava/awt/LayoutManager;)V")) trừCácGiáTrị(2);
            else if (!vănBảnTừ(hằngBộMôTả, "()V")) { giáTrịSựThấtBại("unsupported Swing constructor"); return; }
            int thamChiếuĐốiTượng = trừCácGiáTrị(2); if (!làĐốiTượngHợpLệ(thamChiếuĐốiTượng)) return;
            if (giáTrịVùngNhớĐộng[thamChiếuĐốiTượng] == 30) { giáTrịSựThấtBại("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!đốiTượngMànHình(thamChiếuĐốiTượng) || cácCột < 0) return;
            int giáTrịCănCước = NgườiDùng.kếtNốiMànHình(0, giáTrịVùngNhớĐộng[thamChiếuĐốiTượng] - 23, 0, 0, 0, 0);
            if (giáTrịCănCước < 1 || giáTrịCănCước > 32) { giáTrịSựThấtBại("GUI widget slots exhausted"); return; }
            giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2] = giáTrịCănCước; thamChiếuMànHình[giáTrịCănCước - 1] = thamChiếuĐốiTượng; giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 5] = giáTrịVùngNhớĐộng[thamChiếuĐốiTượng] == 24 ? 130 : 16; giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 6] = giáTrịVùngNhớĐộng[thamChiếuĐốiTượng] == 24 ? 110 : 16;
            giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 7] = giáTrịVùngNhớĐộng[thamChiếuĐốiTượng] == 24 ? 380 : 220; giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 8] = giáTrịVùngNhớĐộng[thamChiếuĐốiTượng] == 24 ? 240 : 28; giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 10] = 1;
            đặtGiáTrịKýTựMànHình(thamChiếuĐốiTượng, thamChiếuVănBản); return;
        }
        if (vănBảnTừ(hằngTên, "setText") || vănBảnTừ(hằngTên, "setTitle")) { int thamChiếuVănBản = trừCácGiáTrị(2), thamChiếuĐốiTượng = trừCácGiáTrị(2); if (đốiTượngMànHình(thamChiếuĐốiTượng) && vănBảnTừ(hằngBộMôTả, "(Ljava/lang/String;)V")) đặtGiáTrịKýTựMànHình(thamChiếuĐốiTượng, thamChiếuVănBản); return; }
        if (vănBảnTừ(hằngTên, "getText") || vănBảnTừ(hằngTên, "getTitle")) { int thamChiếuĐốiTượng = trừCácGiáTrị(2); if (đốiTượngMànHình(thamChiếuĐốiTượng) && vănBảnTừ(hằngBộMôTả, "()Ljava/lang/String;")) đặtGiáTrị(đọcKýTựMànHình(thamChiếuĐốiTượng), 2); return; }
        if (vănBảnTừ(hằngTên, "addActionListener") && vănBảnTừ(hằngBộMôTả, "(Ljava/awt/event/ActionListener;)V")) { int nhậnThamChiếu = trừCácGiáTrị(2), thamChiếuĐốiTượng = trừCácGiáTrị(2); if (đốiTượngMànHình(thamChiếuĐốiTượng)) { giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 4] = nhậnThamChiếu; thamChiếuVùngNhớĐộng[thamChiếuĐốiTượng + 4] = 1; } return; }
        if (vănBảnTừ(hằngTên, "getContentPane") && vănBảnTừ(hằngBộMôTả, "()Ljava/awt/Container;")) { int thamChiếuĐốiTượng = trừCácGiáTrị(2); if (đốiTượngMànHình(thamChiếuĐốiTượng)) đặtGiáTrị(thamChiếuĐốiTượng, 2); return; }
        if (vănBảnTừ(hằngTên, "setLayout") && vănBảnTừ(hằngBộMôTả, "(Ljava/awt/LayoutManager;)V")) { int thamChiếuBốTrí = trừCácGiáTrị(2), thamChiếuĐốiTượng = trừCácGiáTrị(2); if (đốiTượngMànHình(thamChiếuĐốiTượng) && thamChiếuBốTrí != 0) giáTrịSựThấtBại("only absolute layout (null) is supported"); return; }
        if (vănBảnTừ(hằngTên, "add") && (vănBảnTừ(hằngBộMôTả, "(Ljava/awt/Component;)Ljava/awt/Component;") || vănBảnTừ(hằngBộMôTả, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean điềuKiệnBốTrí = vănBảnTừ(hằngBộMôTả, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (điềuKiệnBốTrí) trừCácGiáTrị(2);
            int thamChiếuCon = trừCácGiáTrị(2), thamChiếuĐốiTượng = trừCácGiáTrị(2); if (!đốiTượngMànHình(thamChiếuCon) || !đốiTượngMànHình(thamChiếuĐốiTượng)) return;
            if (NgườiDùng.kếtNốiMànHình(2, giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2], giáTrịVùngNhớĐộng[thamChiếuCon + 2], 0, 0, 0) < 0) { némNgoạiLệ(9, "invalid GUI parent"); return; }
            giáTrịVùngNhớĐộng[thamChiếuCon + 11] = thamChiếuĐốiTượng; thamChiếuVùngNhớĐộng[thamChiếuCon + 11] = 1; if (!điềuKiệnBốTrí) đặtGiáTrị(thamChiếuCon, 2); return;
        }
        if (vănBảnTừ(hằngTên, "setBounds") && vănBảnTừ(hằngBộMôTả, "(IIII)V")) {
            int giáTrịCao = trừCácGiáTrị(1), giáTrịRộng = trừCácGiáTrị(1), tọaĐộY = trừCácGiáTrị(1), tọaĐộX = trừCácGiáTrị(1), thamChiếuĐốiTượng = trừCácGiáTrị(2); if (!đốiTượngMànHình(thamChiếuĐốiTượng)) return;
            if (NgườiDùng.kếtNốiMànHình(1, giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2], tọaĐộX, tọaĐộY, giáTrịRộng, giáTrịCao) < 0) { némNgoạiLệ(9, "GUI bounds"); return; }
            giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 5] = tọaĐộX; giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 6] = tọaĐộY; giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 7] = giáTrịRộng; giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 8] = giáTrịCao; return;
        }
        if (vănBảnTừ(hằngTên, "setSize") && vănBảnTừ(hằngBộMôTả, "(II)V")) {
            int giáTrịCao = trừCácGiáTrị(1), giáTrịRộng = trừCácGiáTrị(1), thamChiếuĐốiTượng = trừCácGiáTrị(2); if (!đốiTượngMànHình(thamChiếuĐốiTượng)) return;
            if (NgườiDùng.kếtNốiMànHình(1, giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2], giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 5], giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 6], giáTrịRộng, giáTrịCao) < 0) némNgoạiLệ(9, "GUI size"); else { giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 7] = giáTrịRộng; giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 8] = giáTrịCao; } return;
        }
        if (vănBảnTừ(hằngTên, "setLocationRelativeTo") && vănBảnTừ(hằngBộMôTả, "(Ljava/awt/Component;)V")) { int tươngĐối = trừCácGiáTrị(2), thamChiếuĐốiTượng = trừCácGiáTrị(2); if (!đốiTượngMànHình(thamChiếuĐốiTượng)) return; if (tươngĐối != 0) { giáTrịSựThấtBại("only screen centering supported"); return; } giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 5] = (NgườiDùng.rộngMànHình() - giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 7]) / 2; giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 6] = (NgườiDùng.caoMànHình() - giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 8]) / 2; NgườiDùng.kếtNốiMànHình(1, giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2], giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 5], giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 6], giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 7], giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 8]); return; }
        if (vănBảnTừ(hằngTên, "setDefaultCloseOperation") && vănBảnTừ(hằngBộMôTả, "(I)V")) { int chínhSách = trừCácGiáTrị(1), thamChiếuĐốiTượng = trừCácGiáTrị(2); if (đốiTượngMànHình(thamChiếuĐốiTượng)) { if (chínhSách < 0 || chínhSách > 3) némNgoạiLệ(9, "close policy"); else { giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 10] = chínhSách; NgườiDùng.kếtNốiMànHình(7, giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2], chínhSách, 0, 0, 0); } } return; }
        if (vănBảnTừ(hằngTên, "setVisible") && vănBảnTừ(hằngBộMôTả, "(Z)V")) { int giáTrịDữLiệu = trừCácGiáTrị(1), thamChiếuĐốiTượng = trừCácGiáTrị(2); if (đốiTượngMànHình(thamChiếuĐốiTượng)) { int giáTrịĐãXửLý = NgườiDùng.kếtNốiMànHình(3, giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2], giáTrịDữLiệu, 0, 0, 0); if (giáTrịĐãXửLý < 0) giáTrịSựThấtBại("Swing requires a standalone interactive command"); else giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 9] = giáTrịDữLiệu; } return; }
        if (vănBảnTừ(hằngTên, "dispose") && vănBảnTừ(hằngBộMôTả, "()V")) { int thamChiếuĐốiTượng = trừCácGiáTrị(2); if (đốiTượngMànHình(thamChiếuĐốiTượng)) { NgườiDùng.kếtNốiMànHình(4, giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2], 0, 0, 0, 0); giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 9] = 0; } return; }
        if (vănBảnTừ(hằngTên, "repaint") || vănBảnTừ(hằngTên, "validate")) { int thamChiếuĐốiTượng = trừCácGiáTrị(2); if (!đốiTượngMànHình(thamChiếuĐốiTượng) || !vănBảnTừ(hằngBộMôTả, "()V")) return; NgườiDùng.kếtNốiMànHình(1, giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 2], giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 5], giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 6], giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 7], giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 8]); return; }
        if (vănBảnTừ(hằngTên, "isVisible") && vănBảnTừ(hằngBộMôTả, "()Z")) { int thamChiếuĐốiTượng = trừCácGiáTrị(2); if (đốiTượngMànHình(thamChiếuĐốiTượng)) đặtGiáTrị(giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 9], 1); return; }
        giáTrịSựThấtBại("unsupported Swing method (native subset)");
    }
    static void sựKiệnĐiềuPhối(int địaChỉĐốiĐích, int sốSựKiện, boolean tiếngViệt) {
        if (địaChỉĐốiĐích < 1 || giáTrịVùngNhớĐộng[địaChỉĐốiĐích] < 32) { giáTrịSựThấtBại("Java event listener required"); return; }
        int chỉSốTệp = phươngThứcTên(giáTrịVùngNhớĐộng[địaChỉĐốiĐích] - 32, sốSựKiện == 0 ? (tiếngViệt ? "thựcThiTácVụ" : "run") : (tiếngViệt ? "nhậnHànhĐộng" : "actionPerformed"), sốSựKiện == 0 ? "()V" : (tiếngViệt ? "(LtiếngViệt/tựThân/ThôngBáoHànhĐộng;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (chỉSốTệp < 0) { giáTrịSựThấtBại("event callback missing"); return; }
        luồngChạyHiệnTại = 0; sốLượngLuồngChạy = 1; chỉSốKhung = 0; trạngTháiLuồngChạy[0] = 1; ngănXếpKhung[0] = 0; khóaKhung[0] = khởiTạoKhung[0] = 0; đổiYêuCầu = false;
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < 128; chỉSốVòngLặp++) { giáTrịCụcBộ[chỉSốVòngLặp] = kiểuCụcBộ[chỉSốVòngLặp] = 0; }
        phươngThứcKhung[0] = chỉSốTệp; vịTríKhung[0] = bắtChạyPhươngThức[chỉSốTệp]; giáTrịCụcBộ[0] = địaChỉĐốiĐích; kiểuCụcBộ[0] = 2;
        if (sốSựKiện != 0) { giáTrịCụcBộ[1] = sốSựKiện; kiểuCụcBộ[1] = 2; }
        làSựKiệnViệcXửLý = true; thựcThiLệnh(); làSựKiệnViệcXửLý = false;
    }
    static void cácSựKiệnMànHình() {
        while (!lỗi) {
            if (sốLượngVềSau > 0) { int địaChỉĐốiĐích = vềSauLậpLịch[0], tiếngViệt = giáTrịTiếngHànVềSau[0]; for (int chỉSốVòngLặp = 1; chỉSốVòngLặp < sốLượngVềSau; chỉSốVòngLặp++) { vềSauLậpLịch[chỉSốVòngLặp - 1] = vềSauLậpLịch[chỉSốVòngLặp]; giáTrịTiếngHànVềSau[chỉSốVòngLặp - 1] = giáTrịTiếngHànVềSau[chỉSốVòngLặp]; } vềSauLậpLịch[--sốLượngVềSau] = 0; giáTrịTiếngHànVềSau[sốLượngVềSau] = 0; sựKiệnĐiềuPhối(địaChỉĐốiĐích, 0, tiếngViệt != 0); continue; }
            if (NgườiDùng.kếtNốiMànHình(6, 0, 0, 0, 0, 0) == 0) return;
            int sốSựKiện = NgườiDùng.kếtNốiMànHình(5, 0, 0, 0, 0, 0); if (sốSựKiện == 0) continue;
            if (sốSựKiện < 0) { giáTrịSựThấtBại("GUI event I/O failed"); return; }
            int giáTrịCănCước = sốSựKiện & 65535; if (giáTrịCănCước < 1 || giáTrịCănCước > 32) continue; int thamChiếuĐốiTượng = thamChiếuMànHình[giáTrịCănCước - 1]; if (thamChiếuĐốiTượng == 0) continue;
            if ((sốSựKiện & 65536) != 0) {
                if (giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 10] != 0) giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 9] = 0;
                if (giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 10] == 3) for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < 32; chỉSốVòngLặp++) if (thamChiếuMànHình[chỉSốVòngLặp] != 0 && giáTrịVùngNhớĐộng[thamChiếuMànHình[chỉSốVòngLặp]] == 24) NgườiDùng.kếtNốiMànHình(4, chỉSốVòngLặp + 1, 0, 0, 0, 0);
            } else if (giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 4] != 0) {
                int thamChiếuHãyĐọc = cấpPhátLưuTrữ(29, 2); if (lỗi) return; giáTrịVùngNhớĐộng[thamChiếuHãyĐọc + 2] = thamChiếuĐốiTượng; giáTrịVùngNhớĐộng[thamChiếuHãyĐọc + 3] = giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 12]; thamChiếuVùngNhớĐộng[thamChiếuHãyĐọc + 2] = 1; sựKiệnĐiềuPhối(giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 4], thamChiếuHãyĐọc, giáTrịVùngNhớĐộng[thamChiếuĐốiTượng + 12] != 0);
            }
        }
    }
    public static int chạy() {
        if (NgườiDùng.sốLượngCácĐốiSố() == 1 && CôngCụJava.vănBảnBằng(NgườiDùng.cácĐốiSố(0), "-version")) {
            NgườiDùng.ghi("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (NgườiDùng.sốLượngCácĐốiSố() < 1) { NgườiDùng.ghi("Usage: java CLASS [ARGS]\n"); return 2; }
        địnhNghĩaLớpMục = nạpĐịnhNghĩaLớp(kýTựChủ(NgườiDùng.cácĐốiSố(0))); if (lỗi || địnhNghĩaLớpMục < 0) return 1;
        int giáTrịĐiểmMục = phươngThứcTên(địnhNghĩaLớpMục, "chạy", "()V");
        boolean mụcTiếngHàn = giáTrịĐiểmMục >= 0 && (truyCậpPhươngThức[giáTrịĐiểmMục] & 9) == 9;
        if (!mụcTiếngHàn) giáTrịĐiểmMục = phươngThứcTên(địnhNghĩaLớpMục, "main", "([Ljava/lang/String;)V");
        if (giáTrịĐiểmMục < 0 || (truyCậpPhươngThức[giáTrịĐiểmMục] & 9) != 9) giáTrịSựThấtBại("public static void chạy() or main(String[] args) required");
        if (lỗi) return 1;
        int cácĐốiSố = cấpPhátLưuTrữ(3, NgườiDùng.sốLượngCácĐốiSố() - 1); phầnTửMảng[cácĐốiSố] = -1;
        for (int trịSố = 1; trịSố < NgườiDùng.sốLượngCácĐốiSố() && !lỗi; trịSố++) giáTrịVùngNhớĐộng[cácĐốiSố + 1 + trịSố] = kýTựChủ(NgườiDùng.cácĐốiSố(trịSố));
        chỉSốKhung = 0; phươngThứcKhung[0] = giáTrịĐiểmMục; vịTríKhung[0] = bắtChạyPhươngThức[giáTrịĐiểmMục]; giáTrịCụcBộ[0] = mụcTiếngHàn ? 0 : cácĐốiSố; kiểuCụcBộ[0] = mụcTiếngHàn ? 0 : 2;
        trạngTháiLuồngChạy[0] = 1; đốiTượngLuồngChạy[0] = cấpPhátLưuTrữ(13, 2);
        thựcThiLệnh(); if (!lỗi) cácSựKiệnMànHình(); return lỗi ? 1 : 0;
    }
}
