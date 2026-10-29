// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Trình biên dịch Java giới hạn chạy trong máy khách, sinh tệp lớp tiêu chuẩn phiên bản 49. */
public final class TrìnhBiênDịchJava {
    static int[] mãNguồn = new int[16384], ĐầuRa = new int[16384], giáTrịMã = new int[4096];
    static int[] loạiTừTố = new int[2048], vịTríTừTố = new int[2048], độDàiTừTố = new int[2048];
    static int[] giáTrịHằng = new int[4096], độLệchHằng = new int[512];
    static int[] KýTự = new int[512], vănBảnTênTệp = new int[64];
    static int[] mãĐãChèn = new int[16];
    static int cỡNguồn, sốLượngTừTố, vịTrí, cỡMã, cỡHằng, sốLượngHằng = 1, cỡĐầuRa, độDàiKýTự;
    static boolean lỗi;
    static int từTốLớp, hằngLớp, hằngCha, hằngMã;
    static int[] tênMụcPhươngThức = new int[32], trảVềPhươngThức = new int[32], sốLượngĐốiSốPhươngThức = new int[32];
    static int[] tênĐốiSốPhươngThức = new int[512], kiểuĐốiSốPhươngThức = new int[512];
    static int[] thânPhươngThức = new int[32], kếtThúcPhươngThức = new int[32], mãPhươngThức = new int[32];
    static int[] độDàiPhươngThức = new int[32], cácBiếnCụcBộPhươngThức = new int[32], hằngTênPhươngThức = new int[32], hằngBộMôTảPhươngThức = new int[32];
    static int[] truyCậpPhươngThức = new int[32];
    static int sốLượngPhươngThức, phươngThứcHiệnTại, sốLượngCụcBộ, giáTrịĐộSâu, độSâuBiểuThức;
    static int[] tênCụcBộ = new int[128], kiểuCụcBộ = new int[128], độSâuCụcBộ = new int[128];

    static void giáTrịSựThấtBại(String giáTrịLýDo) {
        if (!lỗi) {
            NgườiDùng.ghi("javac error: "); NgườiDùng.ghi(giáTrịLýDo);
            NgườiDùng.ghi(" at line ");
            int dòng = 1, phầnKết = vịTrí < sốLượngTừTố ? vịTríTừTố[vịTrí] : cỡNguồn;
            for (int trịSố = 0; trịSố < phầnKết; trịSố++) if (mãNguồn[trịSố] == 10) dòng++;
            CôngCụJava.ghiSố(dòng); NgườiDùng.ghiGiáTrịKýTự(10);
        }
        lỗi = true;
    }
    static boolean giáTrịKýTự(int giáTrị) { return QuyTắcKýTựTên.kýTựĐầuTiên(giáTrị); }
    static boolean giáTrịChữSố(int giáTrị) { return giáTrị >= '0' && giáTrị <= '9'; }
    static boolean bằngCácTên(int toánHạngĐầuTiên, int toánHạngThứHai) {
        if (toánHạngĐầuTiên < 0 || toánHạngThứHai < 0 || toánHạngĐầuTiên >= sốLượngTừTố || toánHạngThứHai >= sốLượngTừTố || độDàiTừTố[toánHạngĐầuTiên] != độDàiTừTố[toánHạngThứHai]) return false;
        for (int trịSố = 0; trịSố < độDàiTừTố[toánHạngĐầuTiên]; trịSố++) if (mãNguồn[vịTríTừTố[toánHạngĐầuTiên] + trịSố] != mãNguồn[vịTríTừTố[toánHạngThứHai] + trịSố]) return false;
        return true;
    }
    static boolean giáTrịTừ(int giáTrịTừTố, String vănBảnTừ) {
        if (giáTrịTừTố < 0 || giáTrịTừTố >= sốLượngTừTố || độDàiTừTố[giáTrịTừTố] != vănBảnTừ.length()) return false;
        for (int trịSố = 0; trịSố < vănBảnTừ.length(); trịSố++) if (mãNguồn[vịTríTừTố[giáTrịTừTố] + trịSố] != vănBảnTừ.charAt(trịSố)) return false;
        return true;
    }
    static int giáTrịLoại() { return vịTrí < sốLượngTừTố ? loạiTừTố[vịTrí] : 0; }
    static boolean nhận(int giáTrị) { if (giáTrịLoại() != giáTrị) return false; vịTrí++; return true; }
    static void giáTrịĐiềuBắtBuộc(int giáTrị) { if (!nhận(giáTrị)) giáTrịSựThấtBại("unexpected token"); }
    static boolean từThu(String vănBảnTừ) { if (!giáTrịTừ(vịTrí, vănBảnTừ)) return false; vịTrí++; return true; }
    static void từĐòiHỏi(String vănBảnTừ) { if (!từThu(vănBảnTừ)) giáTrịSựThấtBại(vănBảnTừ); }
    static int giáTrịĐịnhDanh() {
        int kếtQuả = vịTrí;
        if (giáTrịLoại() != 256) giáTrịSựThấtBại("identifier required"); else vịTrí++;
        String cácTừĐượcDànhTrước = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int chạy = 0;
        for (int trịSố = 0; trịSố <= cácTừĐượcDànhTrước.length(); trịSố++) {
            if (trịSố == cácTừĐượcDànhTrước.length() || cácTừĐượcDànhTrước.charAt(trịSố) == ' ') {
                boolean vănBảnBằng = trịSố - chạy == độDàiTừTố[kếtQuả];
                for (int mụcÔ = chạy; vănBảnBằng && mụcÔ < trịSố; mụcÔ++) if (cácTừĐượcDànhTrước.charAt(mụcÔ) != mãNguồn[vịTríTừTố[kếtQuả] + mụcÔ - chạy]) vănBảnBằng = false;
                if (vănBảnBằng) giáTrịSựThấtBại("reserved word cannot be an identifier");
                chạy = trịSố + 1;
            }
        }
        return kếtQuả;
    }
    static void giáTrịCắt() {
        int trịSố = 0;
        while (trịSố < cỡNguồn && !lỗi) {
            int giáTrị = mãNguồn[trịSố], chạy = trịSố, giáTrịLoại = giáTrị;
            if (giáTrị == 32 || giáTrị == 9 || giáTrị == 10 || giáTrị == 13) { trịSố++; continue; }
            if (giáTrị == '/' && trịSố + 1 < cỡNguồn && mãNguồn[trịSố + 1] == '/') {
                while (trịSố < cỡNguồn && mãNguồn[trịSố] != 10) trịSố++;
                continue;
            }
            if (giáTrị == '/' && trịSố + 1 < cỡNguồn && mãNguồn[trịSố + 1] == '*') {
                trịSố += 2;
                while (trịSố + 1 < cỡNguồn && !(mãNguồn[trịSố] == '*' && mãNguồn[trịSố + 1] == '/')) trịSố++;
                if (trịSố + 1 >= cỡNguồn) { giáTrịSựThấtBại("unterminated comment"); break; }
                trịSố += 2; continue;
            }
            if (giáTrịKýTự(giáTrị)) { giáTrịLoại = 256; while (trịSố < cỡNguồn && QuyTắcKýTựTên.kýTựSựTiếpDiễn(mãNguồn[trịSố])) trịSố++; }
            else if (giáTrịChữSố(giáTrị)) { giáTrịLoại = 257; while (trịSố < cỡNguồn && giáTrịChữSố(mãNguồn[trịSố])) trịSố++; }
            else if (giáTrị == '"' || giáTrị == '\'') {
                giáTrịLoại = giáTrị == '"' ? 258 : 259; trịSố++;
                while (trịSố < cỡNguồn && mãNguồn[trịSố] != giáTrị && mãNguồn[trịSố] != 10 && mãNguồn[trịSố] != 13) {
                    if (mãNguồn[trịSố] == '\\') trịSố++;
                    trịSố++;
                }
                if (trịSố >= cỡNguồn || mãNguồn[trịSố] != giáTrị) { giáTrịSựThấtBại("unterminated literal"); break; }
                trịSố++;
            } else {
                trịSố++;
                if (trịSố < cỡNguồn) {
                    int phầnMụcKếTiếp = mãNguồn[trịSố];
                    if (giáTrị == '=' && phầnMụcKếTiếp == '=') giáTrịLoại = 300;
                    if (giáTrị == '!' && phầnMụcKếTiếp == '=') giáTrịLoại = 301;
                    if (giáTrị == '<' && phầnMụcKếTiếp == '=') giáTrịLoại = 302;
                    if (giáTrị == '>' && phầnMụcKếTiếp == '=') giáTrịLoại = 303;
                    if (giáTrị == '&' && phầnMụcKếTiếp == '&') giáTrịLoại = 304;
                    if (giáTrị == '|' && phầnMụcKếTiếp == '|') giáTrịLoại = 305;
                    if (giáTrị == '+' && phầnMụcKếTiếp == '+') giáTrịLoại = 306;
                    if (giáTrị == '-' && phầnMụcKếTiếp == '-') giáTrịLoại = 307;
                    if (giáTrị == '+' && phầnMụcKếTiếp == '=') giáTrịLoại = 308;
                    if (giáTrị == '-' && phầnMụcKếTiếp == '=') giáTrịLoại = 309;
                    if (giáTrị == '*' && phầnMụcKếTiếp == '=') giáTrịLoại = 310;
                    if (giáTrị == '/' && phầnMụcKếTiếp == '=') giáTrịLoại = 311;
                    if (giáTrị == '%' && phầnMụcKếTiếp == '=') giáTrịLoại = 312;
                    if (giáTrịLoại >= 300) trịSố++;
                }
            }
            if (sốLượngTừTố == loạiTừTố.length - 1) { giáTrịSựThấtBại("too many tokens (2047 maximum)"); break; }
            loạiTừTố[sốLượngTừTố] = giáTrịLoại; vịTríTừTố[sốLượngTừTố] = chạy; độDàiTừTố[sốLượngTừTố++] = trịSố - chạy;
        }
    }
    static void ghiByteHằng(int giáTrị) {
        if (cỡHằng == giáTrịHằng.length) { giáTrịSựThấtBại("constant pool too large"); return; }
        giáTrịHằng[cỡHằng++] = giáTrị & 255;
    }
    static void ghiNgắnKiểuHằng(int giáTrị) { ghiByteHằng(giáTrị >> 8); ghiByteHằng(giáTrị); }
    static int thanhGhiHằng(int chạy) {
        for (int trịSố = 1; trịSố < sốLượngHằng; trịSố++) {
            int giáTrịPhíaTrước = độLệchHằng[trịSố], độDài = (trịSố + 1 < sốLượngHằng ? độLệchHằng[trịSố + 1] : chạy) - giáTrịPhíaTrước;
            if (độDài != cỡHằng - chạy) continue;
            boolean vănBảnBằng = true;
            for (int mụcÔ = 0; mụcÔ < độDài; mụcÔ++) if (giáTrịHằng[giáTrịPhíaTrước + mụcÔ] != giáTrịHằng[chạy + mụcÔ]) vănBảnBằng = false;
            if (vănBảnBằng) { cỡHằng = chạy; return trịSố; }
        }
        if (sốLượngHằng == độLệchHằng.length) { giáTrịSựThấtBại("too many constants"); return 0; }
        độLệchHằng[sốLượngHằng] = chạy;
        return sốLượngHằng++;
    }
    static void thêmCuốiVănBản(int giáTrị) {
        if (độDàiKýTự == KýTự.length) { giáTrịSựThấtBại("text too long"); return; }
        KýTự[độDàiKýTự++] = giáTrị;
    }
    static void thêmCuốiTừ(String vănBảnTừ) { for (int trịSố = 0; trịSố < vănBảnTừ.length(); trịSố++) thêmCuốiVănBản(vănBảnTừ.charAt(trịSố)); }
    static int hằngKýTự() {
        int chạy = cỡHằng; ghiByteHằng(1); ghiNgắnKiểuHằng(0);
        for (int trịSố = 0; trịSố < độDàiKýTự; trịSố++) {
            int giáTrị = KýTự[trịSố];
            if (giáTrị > 0 && giáTrị < 128) ghiByteHằng(giáTrị);
            else if (giáTrị < 2048) { ghiByteHằng(192 | giáTrị >> 6); ghiByteHằng(128 | giáTrị & 63); }
            else { ghiByteHằng(224 | giáTrị >> 12); ghiByteHằng(128 | giáTrị >> 6 & 63); ghiByteHằng(128 | giáTrị & 63); }
        }
        if (lỗi) return 0;
        int độDài = cỡHằng - chạy - 3;
        giáTrịHằng[chạy + 1] = độDài >> 8; giáTrịHằng[chạy + 2] = độDài & 255;
        return thanhGhiHằng(chạy);
    }
    static int hằngTừ(String vănBảnTừ) { độDàiKýTự = 0; thêmCuốiTừ(vănBảnTừ); return hằngKýTự(); }
    static int hằngTừTố(int giáTrịTừTố) {
        độDàiKýTự = 0;
        for (int trịSố = 0; trịSố < độDàiTừTố[giáTrịTừTố]; trịSố++) thêmCuốiVănBản(mãNguồn[vịTríTừTố[giáTrịTừTố] + trịSố]);
        return hằngKýTự();
    }
    static int thamChiếu(int giáTrịLoại, int toánHạngĐầuTiên, int toánHạngThứHai) {
        int chạy = cỡHằng; ghiByteHằng(giáTrịLoại); ghiNgắnKiểuHằng(toánHạngĐầuTiên);
        if (giáTrịLoại == 9 || giáTrịLoại == 10 || giáTrịLoại == 12) ghiNgắnKiểuHằng(toánHạngThứHai);
        return thanhGhiHằng(chạy);
    }
    static int thamChiếuBênNgoài(int giáTrịLoại, String giáTrịChủSởHữu, String tên, String giáTrịMôTả) {
        int địnhDanhChủSởHữu = thamChiếu(7, hằngTừ(giáTrịChủSởHữu), 0);
        int sốLượngTên = hằngTừ(tên), sốLượngĐịnhDạng = hằngTừ(giáTrịMôTả);
        return thamChiếu(giáTrịLoại, địnhDanhChủSởHữu, thamChiếu(12, sốLượngTên, sốLượngĐịnhDạng));
    }
    static void phátGiáTrị(int giáTrị) {
        if (cỡMã == giáTrịMã.length) { giáTrịSựThấtBại("bytecode too large"); return; }
        giáTrịMã[cỡMã++] = giáTrị & 255;
    }
    static void lệnh(int giáTrị, int cácĐốiSố) { phátGiáTrị(giáTrị); phátGiáTrị(cácĐốiSố >> 8); phátGiáTrị(cácĐốiSố); }
    static void hằngThuộcSố(int giáTrị) {
        if (giáTrị >= -1 && giáTrị <= 5) { phátGiáTrị(giáTrị + 3); return; }
        int chạy = cỡHằng; ghiByteHằng(3); ghiNgắnKiểuHằng(giáTrị >>> 16); ghiNgắnKiểuHằng(giáTrị);
        lệnh(19, thanhGhiHằng(chạy));
    }
    static int nhánh(int lệnh) { int kếtQuả = cỡMã; lệnh(lệnh, 0); return kếtQuả; }
    static void giáTrịLiênKết(int nhánh, int đốiTượngĐốiĐích) {
        if (lỗi) return;
        int giáTrịKhoảngCách = đốiTượngĐốiĐích - nhánh;
        if (giáTrịKhoảngCách < -32768 || giáTrịKhoảngCách > 32767 || nhánh < 0 || nhánh + 2 >= cỡMã) { giáTrịSựThấtBại("invalid branch"); return; }
        giáTrịMã[nhánh + 1] = giáTrịKhoảngCách >> 8 & 255; giáTrịMã[nhánh + 2] = giáTrịKhoảngCách & 255;
    }
    static void giáTrịPhépSoSánh(int lệnh) {
        int giáTrịĐúngLuậnLý = nhánh(lệnh); phátGiáTrị(3); int phầnKết = nhánh(167);
        giáTrịLiênKết(giáTrịĐúngLuậnLý, cỡMã); phátGiáTrị(4); giáTrịLiênKết(phầnKết, cỡMã);
    }
    static int giáTrịĐịnhDạng() {
        if (từThu("void")) return 0;
        if (từThu("int")) return 1;
        if (từThu("boolean")) return 2;
        if (từThu("char")) return 5;
        if (từThu("FileInputStream")) return 6;
        if (từThu("FileOutputStream")) return 7;
        if (từThu("String")) { if (nhận('[')) { giáTrịĐiềuBắtBuộc(']'); return 4; } return 3; }
        giáTrịSựThấtBại("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void thêmĐịnhDạng(int giáTrịKiểu) {
        if (giáTrịKiểu == 0) thêmCuốiVănBản('V');
        if (giáTrịKiểu == 1) thêmCuốiVănBản('I');
        if (giáTrịKiểu == 2) thêmCuốiVănBản('Z');
        if (giáTrịKiểu == 3) thêmCuốiTừ("Ljava/lang/String;");
        if (giáTrịKiểu == 4) thêmCuốiTừ("[Ljava/lang/String;");
        if (giáTrịKiểu == 5) thêmCuốiVănBản('C');
        if (giáTrịKiểu == 6) thêmCuốiTừ("Ljava/io/FileInputStream;");
        if (giáTrịKiểu == 7) thêmCuốiTừ("Ljava/io/FileOutputStream;");
    }
    // Trình biên dịch giới hạn hỗ trợ khai báo throws. Thân xử lý ngoại lệ dùng javac của máy chủ.
    static void đọcTênNgoạiLệ() {
        boolean GóiGộpTiếngHàn = từThu("tiếngViệt");
        if (GóiGộpTiếngHàn) { giáTrịĐiềuBắtBuộc('.'); từĐòiHỏi("tựThân"); giáTrịĐiềuBắtBuộc('.'); }
        if (!GóiGộpTiếngHàn && (từThu("Exception") || từThu("IOException"))) return;
        if (từThu("ngoạiLệ") || từThu("NgoạiLệViệcThựcThi") || từThu("NgoạiLệĐầuRaĐầuVào") || từThu("NgoạiLệHếtGiờChờ") || từThu("NgoạiLệTraCứuĐịaChỉ") || từThu("NgoạiLệTệpThiếu") || từThu("NgoạiLệTruyềnThông") || từThu("NgoạiLệĐốiSốKhôngHợpLệ") || từThu("SựThấtBạiĐịnhDạngSố") || từThu("NgoạiLệCácCận") || từThu("NgoạiLệCácCậnMảng") || từThu("NgoạiLệCácCậnChuỗi") || từThu("NgoạiLệThamChiếuRỗngThamChiếu") || từThu("SựThấtBạiSốHọc") || từThu("NgoạiLệTrạngThái") || từThu("NgoạiLệÉpKiểuKiểu") || từThu("SựThấtBạiCỡMảngÂm") || từThu("SựThấtBạiCấtMảng") || từThu("NgoạiLệTrạngTháiLuồngChạy") || từThu("NgoạiLệĐãBịNgắtChờ")) return;
        giáTrịSựThấtBại("unsupported throws type");
    }
    static void đọcKhaiBáo() {
        while (từThu("import")) {
            if (giáTrịTừ(vịTrí, "tiếngViệt")) đọcTênNgoạiLệ();
            else {
                từĐòiHỏi("java"); giáTrịĐiềuBắtBuộc('.'); từĐòiHỏi("io"); giáTrịĐiềuBắtBuộc('.');
                if (!(từThu("FileInputStream") || từThu("FileOutputStream") || từThu("IOException"))) giáTrịSựThấtBại("unsupported import");
            }
            giáTrịĐiềuBắtBuộc(';');
        }
        từThu("public"); từThu("final"); từĐòiHỏi("class"); từTốLớp = giáTrịĐịnhDanh();
        hằngLớp = thamChiếu(7, hằngTừTố(từTốLớp), 0);
        hằngCha = thamChiếu(7, hằngTừ("java/lang/Object"), 0); hằngMã = hằngTừ("Code"); giáTrịĐiềuBắtBuộc('{');
        while (!lỗi && giáTrịLoại() != '}') {
            if (sốLượngPhươngThức == 32) { giáTrịSựThấtBại("too many methods"); break; }
            int mụcTruyCập = từThu("public") ? 1 : từThu("private") ? 2 : 0; từĐòiHỏi("static");
            int Hàm = sốLượngPhươngThức++;
            truyCậpPhươngThức[Hàm] = mụcTruyCập | 8;
            trảVềPhươngThức[Hàm] = giáTrịĐịnhDạng(); tênMụcPhươngThức[Hàm] = giáTrịĐịnhDanh(); giáTrịĐiềuBắtBuộc('(');
            for (int giáTrịPhíaTrước = 0; giáTrịPhíaTrước < Hàm; giáTrịPhíaTrước++) if (bằngCácTên(tênMụcPhươngThức[giáTrịPhíaTrước], tênMụcPhươngThức[Hàm])) giáTrịSựThấtBại("duplicate method (overloading unsupported)");
            while (!lỗi && giáTrịLoại() != ')') {
                int trịSố = sốLượngĐốiSốPhươngThức[Hàm];
                if (trịSố == 16) { giáTrịSựThấtBại("too many parameters"); break; }
                int giáTrịKiểu = giáTrịĐịnhDạng(); if (giáTrịKiểu == 0) giáTrịSựThấtBại("void parameter");
                kiểuĐốiSốPhươngThức[Hàm * 16 + trịSố] = giáTrịKiểu; tênĐốiSốPhươngThức[Hàm * 16 + trịSố] = giáTrịĐịnhDanh();
                sốLượngĐốiSốPhươngThức[Hàm]++;
                if (!nhận(',')) break;
            }
            giáTrịĐiềuBắtBuộc(')');
            if (từThu("throws")) {
                do { đọcTênNgoạiLệ(); } while (!lỗi && nhận(','));
            }
            thânPhươngThức[Hàm] = vịTrí; giáTrịĐiềuBắtBuộc('{');
            int giáTrịLồngNhau = 1;
            while (vịTrí < sốLượngTừTố && giáTrịLồngNhau > 0) {
                if (giáTrịLoại() == '{') giáTrịLồngNhau++;
                if (giáTrịLoại() == '}') giáTrịLồngNhau--;
                vịTrí++;
            }
            if (giáTrịLồngNhau != 0) giáTrịSựThấtBại("unclosed method body");
            kếtThúcPhươngThức[Hàm] = vịTrí;
            hằngTênPhươngThức[Hàm] = hằngTừTố(tênMụcPhươngThức[Hàm]);
            độDàiKýTự = 0; thêmCuốiVănBản('(');
            for (int trịSố = 0; trịSố < sốLượngĐốiSốPhươngThức[Hàm]; trịSố++) thêmĐịnhDạng(kiểuĐốiSốPhươngThức[Hàm * 16 + trịSố]);
            thêmCuốiVănBản(')'); thêmĐịnhDạng(trảVềPhươngThức[Hàm]); hằngBộMôTảPhươngThức[Hàm] = hằngKýTự();
        }
        giáTrịĐiềuBắtBuộc('}'); if (vịTrí != sốLượngTừTố) giáTrịSựThấtBại("extra input after class");
    }
    static int tìmCụcBộ(int tên) {
        for (int trịSố = sốLượngCụcBộ - 1; trịSố >= 0; trịSố--) if (độSâuCụcBộ[trịSố] >= 0 && bằngCácTên(tênCụcBộ[trịSố], tên)) return trịSố;
        giáTrịSựThấtBại("unknown variable"); return 0;
    }
    static int thêmCụcBộ(int tên, int giáTrịKiểu) {
        for (int trịSố = 0; trịSố < sốLượngCụcBộ; trịSố++) if (độSâuCụcBộ[trịSố] >= 0 && bằngCácTên(tênCụcBộ[trịSố], tên)) giáTrịSựThấtBại("duplicate local variable");
        if (sốLượngCụcBộ == 128) { giáTrịSựThấtBại("too many locals"); return 0; }
        tênCụcBộ[sốLượngCụcBộ] = tên; kiểuCụcBộ[sốLượngCụcBộ] = giáTrịKiểu; độSâuCụcBộ[sốLượngCụcBộ] = giáTrịĐộSâu;
        return sốLượngCụcBộ++;
    }
    static boolean kiểuSốNguyên(int giáTrịKiểu) { return giáTrịKiểu == 1 || giáTrịKiểu == 5; }
    static void đọcCụcBộ(int trịSố) { phátGiáTrị(kiểuCụcBộ[trịSố] <= 2 || kiểuCụcBộ[trịSố] == 5 ? 21 : 25); phátGiáTrị(trịSố); }
    static void ghiCụcBộ(int trịSố) { phátGiáTrị(kiểuCụcBộ[trịSố] <= 2 || kiểuCụcBộ[trịSố] == 5 ? 54 : 58); phátGiáTrị(trịSố); }
    static void xácMinhKiểu(int dữLiệuThựcTế, int kỳVọng) { if (dữLiệuThựcTế != kỳVọng && !(dữLiệuThựcTế == 5 && kỳVọng == 1)) giáTrịSựThấtBại("type mismatch"); }
    static void đọcGiáTrịKýTự(int giáTrịTừTố) {
        độDàiKýTự = 0; int chạy = vịTríTừTố[giáTrịTừTố] + 1, phầnKết = vịTríTừTố[giáTrịTừTố] + độDàiTừTố[giáTrịTừTố] - 1;
        while (chạy < phầnKết && !lỗi) {
            int giáTrị = mãNguồn[chạy++];
            if (giáTrị == '\\') {
                if (chạy == phầnKết) { giáTrịSựThấtBại("invalid escape"); break; }
                giáTrị = mãNguồn[chạy++];
                if (giáTrị == 'n') giáTrị = 10;
                else if (giáTrị == 'r') giáTrị = 13;
                else if (giáTrị == 't') giáTrị = 9;
                else if (giáTrị == 'b') giáTrị = 8;
                else if (giáTrị == 'f') giáTrị = 12;
                else if (giáTrị != '\\' && giáTrị != '"' && giáTrị != '\'') giáTrịSựThấtBại("unsupported escape");
            }
            thêmCuốiVănBản(giáTrị);
        }
    }
    static int phânTíchCúPhápSốNguyên(int giáTrịTừTố, boolean giáTrịÂm) {
        if (độDàiTừTố[giáTrịTừTố] > 1 && mãNguồn[vịTríTừTố[giáTrịTừTố]] == '0') giáTrịSựThấtBại("octal literals unsupported");
        int giáTrị = 0;
        for (int trịSố = 0; trịSố < độDàiTừTố[giáTrịTừTố]; trịSố++) {
            int phầnMụcChữSố = mãNguồn[vịTríTừTố[giáTrịTừTố] + trịSố] - '0';
            if (giáTrị < -214748364 || giáTrị == -214748364 && phầnMụcChữSố > (giáTrịÂm ? 8 : 7)) giáTrịSựThấtBại("integer literal out of range");
            giáTrị = giáTrị * 10 - phầnMụcChữSố;
        }
        return giáTrịÂm ? giáTrị : -giáTrị;
    }
    static int biểuThứcChínhThức() {
        if (từThu("new")) {
            int giáTrịKiểu = giáTrịĐịnhDạng();
            if (giáTrịKiểu != 6 && giáTrịKiểu != 7) { giáTrịSựThấtBại("only file streams supported by new in source"); return 0; }
            String giáTrịChủSởHữu = giáTrịKiểu == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            lệnh(187, thamChiếu(7, hằngTừ(giáTrịChủSởHữu), 0)); phátGiáTrị(89);
            giáTrịĐiềuBắtBuộc('('); xácMinhKiểu(giáTrịBiểuThức(), 3); boolean giáTrịSựTiếpDiễn = false;
            if (nhận(',')) { if (giáTrịKiểu != 7) giáTrịSựThấtBại("input stream constructor arguments"); xácMinhKiểu(giáTrịBiểuThức(), 2); giáTrịSựTiếpDiễn = true; }
            giáTrịĐiềuBắtBuộc(')');
            lệnh(183, thamChiếuBênNgoài(10, giáTrịChủSởHữu, "<init>", giáTrịSựTiếpDiễn ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return giáTrịKiểu;
        }
        if (nhận('(')) { int giáTrịKiểu = giáTrịBiểuThức(); giáTrịĐiềuBắtBuộc(')'); return giáTrịKiểu; }
        if (giáTrịLoại() == 257) { hằngThuộcSố(phânTíchCúPhápSốNguyên(vịTrí++, false)); return 1; }
        if (giáTrịLoại() == 258) { đọcGiáTrịKýTự(vịTrí++); lệnh(19, thamChiếu(8, hằngKýTự(), 0)); return 3; }
        if (giáTrịLoại() == 259) { đọcGiáTrịKýTự(vịTrí++); if (độDàiKýTự != 1) giáTrịSựThấtBại("character literal length"); hằngThuộcSố(KýTự[0]); return 5; }
        if (từThu("true")) { phátGiáTrị(4); return 2; }
        if (từThu("false")) { phátGiáTrị(3); return 2; }
        if (từThu("tiếngViệt")) {
            giáTrịĐiềuBắtBuộc('.'); từĐòiHỏi("tựThân"); giáTrịĐiềuBắtBuộc('.');
            String giáTrịChủSởHữu = "", giáTrịPhươngThức = "", giáTrịMôTả = ""; int toánHạngĐầuTiên = 0, toánHạngThứHai = 0, toánHạngThứBa = 0, toánHạngThứTư = 0, toánHạngThứNăm = 0, kếtQuả = 0;
            if (từThu("ĐầuRa")) {
                giáTrịChủSởHữu = "tiếngViệt/tựThân/ĐầuRa"; giáTrịĐiềuBắtBuộc('.');
                if (từThu("ghiDòng")) { giáTrịPhươngThức = "ghiDòng"; giáTrịMôTả = "(Ljava/lang/String;)V"; toánHạngĐầuTiên = 3; }
                else if (từThu("ghi")) { giáTrịPhươngThức = "ghi"; giáTrịMôTả = "(Ljava/lang/String;)V"; toánHạngĐầuTiên = 3; }
                else if (từThu("ghiSố")) { giáTrịPhươngThức = "ghiSố"; giáTrịMôTả = "(I)V"; toánHạngĐầuTiên = 1; }
                else giáTrịSựThấtBại("unknown Korean output method");
            } else if (từThu("KýTự")) {
                giáTrịChủSởHữu = "tiếngViệt/tựThân/KýTự"; giáTrịĐiềuBắtBuộc('.'); toánHạngĐầuTiên = 3;
                if (từThu("độDài")) { giáTrịPhươngThức = "độDài"; giáTrịMôTả = "(Ljava/lang/String;)I"; kếtQuả = 1; }
                else if (từThu("sốLượngĐiểmMã")) { giáTrịPhươngThức = "sốLượngĐiểmMã"; giáTrịMôTả = "(Ljava/lang/String;)I"; kếtQuả = 1; }
                else if (từThu("phânTíchCúPhápSốNguyên")) { giáTrịPhươngThức = "phânTíchCúPhápSốNguyên"; giáTrịMôTả = "(Ljava/lang/String;)I"; kếtQuả = 1; }
                else if (từThu("ghiGiáTrịSốNguyên")) { giáTrịPhươngThức = "ghiGiáTrịSốNguyên"; giáTrịMôTả = "(I)Ljava/lang/String;"; toánHạngĐầuTiên = 1; kếtQuả = 3; }
                else if (từThu("vănBảnBằng")) { giáTrịPhươngThức = "vănBảnBằng"; giáTrịMôTả = "(Ljava/lang/String;Ljava/lang/String;)Z"; toánHạngThứHai = 3; kếtQuả = 2; }
                else if (từThu("vănBảnDán")) { giáTrịPhươngThức = "vănBảnDán"; giáTrịMôTả = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; toánHạngThứHai = 3; kếtQuả = 3; }
                else if (từThu("giáTrịCắt")) { giáTrịPhươngThức = "giáTrịCắt"; giáTrịMôTả = "(Ljava/lang/String;II)Ljava/lang/String;"; toánHạngThứHai = 1; toánHạngThứBa = 1; kếtQuả = 3; }
                else giáTrịSựThấtBại("unknown Korean text method");
            } else if (từThu("Tệp")) {
                giáTrịChủSởHữu = "tiếngViệt/tựThân/Tệp"; giáTrịĐiềuBắtBuộc('.'); toánHạngĐầuTiên = 3;
                if (từThu("đọc")) { giáTrịPhươngThức = "đọc"; giáTrịMôTả = "(Ljava/lang/String;)Ljava/lang/String;"; kếtQuả = 3; }
                else if (từThu("ghi")) { giáTrịPhươngThức = "ghi"; giáTrịMôTả = "(Ljava/lang/String;Ljava/lang/String;)V"; toánHạngThứHai = 3; }
                else giáTrịSựThấtBại("unknown Korean file method");
            } else if (từThu("MànHình")) {
                giáTrịChủSởHữu = "tiếngViệt/tựThân/MànHình"; giáTrịĐiềuBắtBuộc('.');
                if (từThu("giáTrịRộng")) { giáTrịPhươngThức = "giáTrịRộng"; giáTrịMôTả = "()I"; kếtQuả = 1; }
                else if (từThu("giáTrịCao")) { giáTrịPhươngThức = "giáTrịCao"; giáTrịMôTả = "()I"; kếtQuả = 1; }
                else if (từThu("hìnhChữNhật")) { giáTrịPhươngThức = "hìnhChữNhật"; giáTrịMôTả = "(IIIII)V"; toánHạngĐầuTiên = 1; toánHạngThứHai = 1; toánHạngThứBa = 1; toánHạngThứTư = 1; toánHạngThứNăm = 1; }
                else if (từThu("xóaMục")) { giáTrịPhươngThức = "xóaMục"; giáTrịMôTả = "(I)V"; toánHạngĐầuTiên = 1; }
                else if (từThu("đợi")) { giáTrịPhươngThức = "đợi"; giáTrịMôTả = "()V"; }
                else giáTrịSựThấtBại("unknown Korean framebuffer method");
            } else giáTrịSựThấtBại("unsupported Korean library class");
            giáTrịĐiềuBắtBuộc('('); if (toánHạngĐầuTiên != 0) xácMinhKiểu(giáTrịBiểuThức(), toánHạngĐầuTiên);
            if (toánHạngThứHai != 0) { giáTrịĐiềuBắtBuộc(','); xácMinhKiểu(giáTrịBiểuThức(), toánHạngThứHai); }
            if (toánHạngThứBa != 0) { giáTrịĐiềuBắtBuộc(','); xácMinhKiểu(giáTrịBiểuThức(), toánHạngThứBa); }
            if (toánHạngThứTư != 0) { giáTrịĐiềuBắtBuộc(','); xácMinhKiểu(giáTrịBiểuThức(), toánHạngThứTư); }
            if (toánHạngThứNăm != 0) { giáTrịĐiềuBắtBuộc(','); xácMinhKiểu(giáTrịBiểuThức(), toánHạngThứNăm); }
            giáTrịĐiềuBắtBuộc(')'); lệnh(184, thamChiếuBênNgoài(10, giáTrịChủSởHữu, giáTrịPhươngThức, giáTrịMôTả)); return kếtQuả;
        }
        if (từThu("Integer")) {
            giáTrịĐiềuBắtBuộc('.'); từĐòiHỏi("parseInt"); giáTrịĐiềuBắtBuộc('('); xácMinhKiểu(giáTrịBiểuThức(), 3); giáTrịĐiềuBắtBuộc(')');
            lệnh(184, thamChiếuBênNgoài(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int tên = giáTrịĐịnhDanh();
        if (nhận('(')) {
            int Hàm = -1;
            for (int trịSố = 0; trịSố < sốLượngPhươngThức; trịSố++) if (bằngCácTên(tên, tênMụcPhươngThức[trịSố])) Hàm = trịSố;
            if (Hàm < 0) { giáTrịSựThấtBại("unknown static method"); return 0; }
            int trịSố = 0;
            while (!lỗi && giáTrịLoại() != ')') {
                if (trịSố >= sốLượngĐốiSốPhươngThức[Hàm]) { giáTrịSựThấtBại("too many arguments"); break; }
                xácMinhKiểu(giáTrịBiểuThức(), kiểuĐốiSốPhươngThức[Hàm * 16 + trịSố++]); if (!nhận(',')) break;
            }
            giáTrịĐiềuBắtBuộc(')'); if (trịSố != sốLượngĐốiSốPhươngThức[Hàm]) giáTrịSựThấtBại("argument count mismatch");
            lệnh(184, thamChiếu(10, hằngLớp, thamChiếu(12, hằngTênPhươngThức[Hàm], hằngBộMôTảPhươngThức[Hàm])));
            return trảVềPhươngThức[Hàm];
        }
        int phạmViCụcBộ = tìmCụcBộ(tên), giáTrịKiểu = kiểuCụcBộ[phạmViCụcBộ]; đọcCụcBộ(phạmViCụcBộ);
        while (!lỗi) {
            if (nhận('[')) { xácMinhKiểu(giáTrịKiểu, 4); xácMinhKiểu(giáTrịBiểuThức(), 1); giáTrịĐiềuBắtBuộc(']'); phátGiáTrị(50); giáTrịKiểu = 3; }
            else if (nhận('.')) {
                if (giáTrịKiểu == 6 || giáTrịKiểu == 7) {
                    String giáTrịChủSởHữu = giáTrịKiểu == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (từThu("close")) { giáTrịĐiềuBắtBuộc('('); giáTrịĐiềuBắtBuộc(')'); lệnh(182, thamChiếuBênNgoài(10, giáTrịChủSởHữu, "close", "()V")); giáTrịKiểu = 0; }
                    else if (giáTrịKiểu == 6 && từThu("read")) { giáTrịĐiềuBắtBuộc('('); giáTrịĐiềuBắtBuộc(')'); lệnh(182, thamChiếuBênNgoài(10, giáTrịChủSởHữu, "read", "()I")); giáTrịKiểu = 1; }
                    else if (giáTrịKiểu == 7 && từThu("write")) { giáTrịĐiềuBắtBuộc('('); xácMinhKiểu(giáTrịBiểuThức(), 1); giáTrịĐiềuBắtBuộc(')'); lệnh(182, thamChiếuBênNgoài(10, giáTrịChủSởHữu, "write", "(I)V")); giáTrịKiểu = 0; }
                    else { giáTrịSựThấtBại("unsupported file stream method"); }
                    continue;
                }
                từĐòiHỏi("length");
                if (giáTrịKiểu == 4) { phátGiáTrị(190); giáTrịKiểu = 1; }
                else { xácMinhKiểu(giáTrịKiểu, 3); giáTrịĐiềuBắtBuộc('('); giáTrịĐiềuBắtBuộc(')'); lệnh(182, thamChiếuBênNgoài(10, "java/lang/String", "length", "()I")); giáTrịKiểu = 1; }
            } else break;
        }
        return giáTrịKiểu;
    }
    static int giáTrịMộtNgôi() {
        if (++độSâuBiểuThức > 64) { giáTrịSựThấtBại("expression nesting too deep"); độSâuBiểuThức--; return 0; }
        int giáTrịKiểu;
        if (nhận('!')) { xácMinhKiểu(giáTrịMộtNgôi(), 2); giáTrịPhépSoSánh(153); giáTrịKiểu = 2; }
        else if (nhận('-')) {
            if (giáTrịLoại() == 257) hằngThuộcSố(phânTíchCúPhápSốNguyên(vịTrí++, true));
            else { xácMinhKiểu(giáTrịMộtNgôi(), 1); phátGiáTrị(116); }
            giáTrịKiểu = 1;
        } else if (nhận('+')) { xácMinhKiểu(giáTrịMộtNgôi(), 1); giáTrịKiểu = 1; }
        else giáTrịKiểu = biểuThứcChínhThức();
        độSâuBiểuThức--; return giáTrịKiểu;
    }
    static int biểuThứcPhépNhân() {
        int giáTrịKiểu = giáTrịMộtNgôi();
        while (!lỗi && (giáTrịLoại() == '*' || giáTrịLoại() == '/' || giáTrịLoại() == '%')) {
            int giáTrịBảngMã = giáTrịLoại(); vịTrí++; xácMinhKiểu(giáTrịKiểu, 1); xácMinhKiểu(giáTrịMộtNgôi(), 1);
            phátGiáTrị(giáTrịBảngMã == '*' ? 104 : giáTrịBảngMã == '/' ? 108 : 112); giáTrịKiểu = 1;
        }
        return giáTrịKiểu;
    }
    static int biểuThứcPhépCộng() {
        int giáTrịKiểu = biểuThứcPhépNhân();
        while (!lỗi && (giáTrịLoại() == '+' || giáTrịLoại() == '-')) {
            int giáTrịBảngMã = giáTrịLoại(); vịTrí++; int giáTrịRanhGiới = cỡMã, kiểuGiáTrịLùi = biểuThứcPhépNhân();
            if (giáTrịBảngMã == '+' && (giáTrịKiểu == 3 || kiểuGiáTrịLùi == 3)) { cácGiáTrịKếtHợp(giáTrịRanhGiới, giáTrịKiểu, kiểuGiáTrịLùi); giáTrịKiểu = 3; }
            else { xácMinhKiểu(giáTrịKiểu, 1); xácMinhKiểu(kiểuGiáTrịLùi, 1); phátGiáTrị(giáTrịBảngMã == '+' ? 96 : 100); giáTrịKiểu = 1; }
        }
        return giáTrịKiểu;
    }
    static int thamChiếuĐãGắn(int giáTrịKiểu) {
        if (giáTrịKiểu != 1 && giáTrịKiểu != 2 && giáTrịKiểu != 3 && giáTrịKiểu != 5) giáTrịSựThấtBại("unsupported concatenation type");
        return thamChiếuBênNgoài(10, "java/lang/StringBuilder", "append", giáTrịKiểu == 1 ? "(I)Ljava/lang/StringBuilder;"
            : giáTrịKiểu == 2 ? "(Z)Ljava/lang/StringBuilder;" : giáTrịKiểu == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void cácGiáTrịKếtHợp(int giáTrịRanhGiới, int kiểuGiáTrịPhíaTrước, int kiểuGiáTrịLùi) {
        // Chèn mã sinh trước mã vế phải để append giá trị vế trái đã tính trước.
        // Khoảng cách nhánh tương đối trong biểu thức phải vẫn đúng vì toàn bộ vùng được dời cùng nhau.
        int phầnKết = cỡMã;
        lệnh(187, thamChiếu(7, hằngTừ("java/lang/StringBuilder"), 0)); phátGiáTrị(89);
        lệnh(183, thamChiếuBênNgoài(10, "java/lang/StringBuilder", "<init>", "()V")); phátGiáTrị(95); lệnh(182, thamChiếuĐãGắn(kiểuGiáTrịPhíaTrước));
        if (lỗi) return;
        int độDài = cỡMã - phầnKết;
        for (int trịSố = 0; trịSố < độDài; trịSố++) mãĐãChèn[trịSố] = giáTrịMã[phầnKết + trịSố];
        for (int trịSố = phầnKết - 1; trịSố >= giáTrịRanhGiới; trịSố--) giáTrịMã[trịSố + độDài] = giáTrịMã[trịSố];
        for (int trịSố = 0; trịSố < độDài; trịSố++) giáTrịMã[giáTrịRanhGiới + trịSố] = mãĐãChèn[trịSố];
        lệnh(182, thamChiếuĐãGắn(kiểuGiáTrịLùi)); lệnh(182, thamChiếuBênNgoài(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int biểuThứcPhépSoSánh() {
        int giáTrịKiểu = biểuThứcPhépCộng();
        while (!lỗi && (giáTrịLoại() == '<' || giáTrịLoại() == '>' || giáTrịLoại() == 302 || giáTrịLoại() == 303)) {
            int giáTrịBảngMã = giáTrịLoại(); vịTrí++; xácMinhKiểu(giáTrịKiểu, 1); xácMinhKiểu(biểuThứcPhépCộng(), 1);
            giáTrịPhépSoSánh(giáTrịBảngMã == '<' ? 161 : giáTrịBảngMã == '>' ? 163 : giáTrịBảngMã == 302 ? 164 : 162); giáTrịKiểu = 2;
        }
        return giáTrịKiểu;
    }
    static int biểuThứcTínhBằngNhau() {
        int giáTrịKiểu = biểuThứcPhépSoSánh();
        while (!lỗi && (giáTrịLoại() == 300 || giáTrịLoại() == 301)) {
            int giáTrịBảngMã = giáTrịLoại(); vịTrí++; int kiểuGiáTrịLùi = biểuThứcPhépSoSánh();
            if (giáTrịKiểu == 0 || kiểuGiáTrịLùi == 0) giáTrịSựThấtBại("void expression");
            if (!(kiểuSốNguyên(giáTrịKiểu) && kiểuSốNguyên(kiểuGiáTrịLùi))) xácMinhKiểu(kiểuGiáTrịLùi, giáTrịKiểu);
            giáTrịPhépSoSánh((giáTrịKiểu <= 2 || giáTrịKiểu == 5 ? 159 : 165) + (giáTrịBảngMã == 301 ? 1 : 0)); giáTrịKiểu = 2;
        }
        return giáTrịKiểu;
    }
    static int vàLuậnLýHọc() {
        int giáTrịKiểu = biểuThứcTínhBằngNhau();
        while (!lỗi && nhận(304)) {
            xácMinhKiểu(giáTrịKiểu, 2); int toánHạngĐầuTiên = nhánh(153); xácMinhKiểu(biểuThứcTínhBằngNhau(), 2); int toánHạngThứHai = nhánh(153);
            phátGiáTrị(4); int phầnKết = nhánh(167); giáTrịLiênKết(toánHạngĐầuTiên, cỡMã); giáTrịLiênKết(toánHạngThứHai, cỡMã); phátGiáTrị(3); giáTrịLiênKết(phầnKết, cỡMã); giáTrịKiểu = 2;
        }
        return giáTrịKiểu;
    }
    static int giáTrịBiểuThức() {
        int giáTrịKiểu = vàLuậnLýHọc();
        while (!lỗi && nhận(305)) {
            xácMinhKiểu(giáTrịKiểu, 2); int toánHạngĐầuTiên = nhánh(154); xácMinhKiểu(vàLuậnLýHọc(), 2); int toánHạngThứHai = nhánh(154);
            phátGiáTrị(3); int phầnKết = nhánh(167); giáTrịLiênKết(toánHạngĐầuTiên, cỡMã); giáTrịLiênKết(toánHạngThứHai, cỡMã); phátGiáTrị(4); giáTrịLiênKết(phầnKết, cỡMã); giáTrịKiểu = 2;
        }
        return giáTrịKiểu;
    }
    static void giáTrịPhépGán(boolean choPhépKhaiBáo) {
        if (giáTrịTừ(vịTrí, "int") || giáTrịTừ(vịTrí, "boolean") || giáTrịTừ(vịTrí, "String") || giáTrịTừ(vịTrí, "char")
            || giáTrịTừ(vịTrí, "FileInputStream") || giáTrịTừ(vịTrí, "FileOutputStream")) {
            if (!choPhépKhaiBáo) giáTrịSựThấtBại("declaration not allowed here");
            int giáTrịKiểu = giáTrịĐịnhDạng(), tên = giáTrịĐịnhDanh(); giáTrịĐiềuBắtBuộc('='); xácMinhKiểu(giáTrịBiểuThức(), giáTrịKiểu);
            ghiCụcBộ(thêmCụcBộ(tên, giáTrịKiểu)); return;
        }
        int tên = giáTrịĐịnhDanh(), phạmViCụcBộ = tìmCụcBộ(tên);
        if (nhận('=')) { xácMinhKiểu(giáTrịBiểuThức(), kiểuCụcBộ[phạmViCụcBộ]); ghiCụcBộ(phạmViCụcBộ); }
        else if (giáTrịLoại() >= 308 && giáTrịLoại() <= 312) {
            int giáTrịBảngMã = giáTrịLoại(); vịTrí++; đọcCụcBộ(phạmViCụcBộ); int giáTrịRanhGiới = cỡMã, kiểuGiáTrịLùi = giáTrịBiểuThức();
            if (giáTrịBảngMã == 308 && kiểuCụcBộ[phạmViCụcBộ] == 3) cácGiáTrịKếtHợp(giáTrịRanhGiới, 3, kiểuGiáTrịLùi);
            else {
                xácMinhKiểu(kiểuCụcBộ[phạmViCụcBộ], 1); xácMinhKiểu(kiểuGiáTrịLùi, 1);
                phátGiáTrị(giáTrịBảngMã == 308 ? 96 : giáTrịBảngMã == 309 ? 100 : giáTrịBảngMã == 310 ? 104 : giáTrịBảngMã == 311 ? 108 : 112);
                if (kiểuCụcBộ[phạmViCụcBộ] == 5) phátGiáTrị(146);
            }
            ghiCụcBộ(phạmViCụcBộ);
        }
        else if (giáTrịLoại() == 306 || giáTrịLoại() == 307) {
            xácMinhKiểu(kiểuCụcBộ[phạmViCụcBộ], 1); phátGiáTrị(132); phátGiáTrị(phạmViCụcBộ); phátGiáTrị(giáTrịLoại() == 306 ? 1 : 255); vịTrí++;
            if (kiểuCụcBộ[phạmViCụcBộ] == 5) { đọcCụcBộ(phạmViCụcBộ); phátGiáTrị(146); ghiCụcBộ(phạmViCụcBộ); }
        } else giáTrịSựThấtBại("assignment or postfix increment required");
    }
    static void đầuRaMànHình() {
        từĐòiHỏi("System"); giáTrịĐiềuBắtBuộc('.'); từĐòiHỏi("out"); giáTrịĐiềuBắtBuộc('.');
        boolean xuốngDòng = từThu("println"); if (!xuốngDòng) từĐòiHỏi("print"); giáTrịĐiềuBắtBuộc('(');
        lệnh(178, thamChiếuBênNgoài(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean đốiSốRỗng = giáTrịLoại() == ')';
        int giáTrịKiểu = đốiSốRỗng ? 0 : giáTrịBiểuThức(); giáTrịĐiềuBắtBuộc(')'); giáTrịĐiềuBắtBuộc(';');
        String giáTrịMôTả = giáTrịKiểu == 0 ? "()V" : giáTrịKiểu == 1 ? "(I)V" : giáTrịKiểu == 2 ? "(Z)V" : giáTrịKiểu == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (giáTrịKiểu == 4 || giáTrịKiểu >= 6 || giáTrịKiểu == 0 && (!xuốngDòng || !đốiSốRỗng)) giáTrịSựThấtBại("unsupported print argument");
        lệnh(182, thamChiếuBênNgoài(10, "java/io/PrintStream", xuốngDòng ? "println" : "print", giáTrịMôTả));
    }
    static boolean giáTrịCâuLệnh() {
        if (lỗi) return false;
        if (giáTrịĐộSâu > 32) { giáTrịSựThấtBại("statement nesting too deep"); return false; }
        if (nhận('{')) {
            giáTrịĐộSâu++; boolean kếtQuảTrảVề = false;
            while (!lỗi && giáTrịLoại() != '}') { if (kếtQuảTrảVề) giáTrịSựThấtBại("unreachable statement"); kếtQuảTrảVề = giáTrịCâuLệnh(); }
            giáTrịĐiềuBắtBuộc('}'); for (int trịSố = 0; trịSố < sốLượngCụcBộ; trịSố++) if (độSâuCụcBộ[trịSố] == giáTrịĐộSâu) độSâuCụcBộ[trịSố] = -1;
            giáTrịĐộSâu--; return kếtQuảTrảVề;
        }
        if (nhận(';')) return false;
        if (từThu("return")) {
            int giáTrịKiểu = giáTrịLoại() == ';' ? 0 : giáTrịBiểuThức(); xácMinhKiểu(giáTrịKiểu, trảVềPhươngThức[phươngThứcHiệnTại]); giáTrịĐiềuBắtBuộc(';');
            phátGiáTrị(giáTrịKiểu == 0 ? 177 : giáTrịKiểu <= 2 || giáTrịKiểu == 5 ? 172 : 176); return true;
        }
        if (từThu("if")) {
            giáTrịĐiềuBắtBuộc('('); xácMinhKiểu(giáTrịBiểuThức(), 2); giáTrịĐiềuBắtBuộc(')'); int giáTrịSaiLuậnLý = nhánh(153);
            giáTrịĐộSâu++; boolean toánHạngĐầuTiên = câuLệnhĐiềuKhiển(); giáTrịĐộSâu--;
            if (từThu("else")) { int phầnKết = nhánh(167); giáTrịLiênKết(giáTrịSaiLuậnLý, cỡMã); giáTrịĐộSâu++; boolean toánHạngThứHai = câuLệnhĐiềuKhiển(); giáTrịĐộSâu--; giáTrịLiênKết(phầnKết, cỡMã); return toánHạngĐầuTiên && toánHạngThứHai; }
            giáTrịLiênKết(giáTrịSaiLuậnLý, cỡMã); return false;
        }
        if (từThu("while")) {
            int chạy = cỡMã; giáTrịĐiềuBắtBuộc('('); xácMinhKiểu(giáTrịBiểuThức(), 2); giáTrịĐiềuBắtBuộc(')'); int phầnKết = nhánh(153);
            giáTrịĐộSâu++; câuLệnhĐiềuKhiển(); giáTrịĐộSâu--; giáTrịLiênKết(nhánh(167), chạy); giáTrịLiênKết(phầnKết, cỡMã); return false;
        }
        if (từThu("for")) {
            giáTrịĐộSâu++; giáTrịĐiềuBắtBuộc('('); if (giáTrịLoại() != ';') giáTrịPhépGán(true); giáTrịĐiềuBắtBuộc(';');
            int điềuKiện = cỡMã; if (giáTrịLoại() == ';') phátGiáTrị(4); else xácMinhKiểu(giáTrịBiểuThức(), 2); giáTrịĐiềuBắtBuộc(';');
            int phầnKết = nhánh(153), vănBảnThân = nhánh(167), làmMới = cỡMã;
            if (giáTrịLoại() != ')') giáTrịPhépGán(false); giáTrịĐiềuBắtBuộc(')'); giáTrịLiênKết(nhánh(167), điềuKiện); giáTrịLiênKết(vănBảnThân, cỡMã);
            câuLệnhĐiềuKhiển(); giáTrịLiênKết(nhánh(167), làmMới); giáTrịLiênKết(phầnKết, cỡMã);
            for (int trịSố = 0; trịSố < sốLượngCụcBộ; trịSố++) if (độSâuCụcBộ[trịSố] == giáTrịĐộSâu) độSâuCụcBộ[trịSố] = -1;
            giáTrịĐộSâu--; return false;
        }
        if (giáTrịTừ(vịTrí, "System")) { đầuRaMànHình(); return false; }
        if (giáTrịLoại() == 256 && vịTrí + 1 < sốLượngTừTố && (loạiTừTố[vịTrí + 1] == '(' || loạiTừTố[vịTrí + 1] == '.')) {
            int giáTrịKiểu = giáTrịBiểuThức(); if (giáTrịKiểu != 0) phátGiáTrị(87); giáTrịĐiềuBắtBuộc(';'); return false;
        }
        giáTrịPhépGán(true); giáTrịĐiềuBắtBuộc(';'); return false;
    }
    static boolean câuLệnhĐiềuKhiển() {
        if (giáTrịTừ(vịTrí, "int") || giáTrịTừ(vịTrí, "boolean") || giáTrịTừ(vịTrí, "char") || giáTrịTừ(vịTrí, "String")
            || giáTrịTừ(vịTrí, "FileInputStream") || giáTrịTừ(vịTrí, "FileOutputStream")) giáTrịSựThấtBại("local declaration requires braces");
        return giáTrịCâuLệnh();
    }
    static void phátByteLớp(int giáTrị) { if (cỡĐầuRa == ĐầuRa.length) giáTrịSựThấtBại("class file too large"); else ĐầuRa[cỡĐầuRa++] = giáTrị & 255; }
    static void phátNgắnKiểuLớp(int giáTrị) { phátByteLớp(giáTrị >> 8); phátByteLớp(giáTrị); }
    static void phátSốNguyênLớp(int giáTrị) { phátNgắnKiểuLớp(giáTrị >>> 16); phátNgắnKiểuLớp(giáTrị); }
    static void ghiLớp() {
        phátSốNguyênLớp(0xcafebabe); phátNgắnKiểuLớp(0); phátNgắnKiểuLớp(49); phátNgắnKiểuLớp(sốLượngHằng);
        for (int trịSố = 0; trịSố < cỡHằng; trịSố++) phátByteLớp(giáTrịHằng[trịSố]);
        phátNgắnKiểuLớp(0x21); phátNgắnKiểuLớp(hằngLớp); phátNgắnKiểuLớp(hằngCha); phátNgắnKiểuLớp(0); phátNgắnKiểuLớp(0); phátNgắnKiểuLớp(sốLượngPhươngThức);
        for (int trịSố = 0; trịSố < sốLượngPhươngThức; trịSố++) {
            phátNgắnKiểuLớp(truyCậpPhươngThức[trịSố]); phátNgắnKiểuLớp(hằngTênPhươngThức[trịSố]); phátNgắnKiểuLớp(hằngBộMôTảPhươngThức[trịSố]); phátNgắnKiểuLớp(1); phátNgắnKiểuLớp(hằngMã);
            phátSốNguyênLớp(12 + độDàiPhươngThức[trịSố]); phátNgắnKiểuLớp(128); phátNgắnKiểuLớp(cácBiếnCụcBộPhươngThức[trịSố]); phátSốNguyênLớp(độDàiPhươngThức[trịSố]);
            for (int mụcÔ = 0; mụcÔ < độDàiPhươngThức[trịSố]; mụcÔ++) phátByteLớp(giáTrịMã[mãPhươngThức[trịSố] + mụcÔ]);
            phátNgắnKiểuLớp(0); phátNgắnKiểuLớp(0);
        }
        phátNgắnKiểuLớp(0);
    }
    public static int chạy() {
        if (NgườiDùng.sốLượngCácĐốiSố() == 1 && CôngCụJava.vănBảnBằng(NgườiDùng.cácĐốiSố(0), "-version")) {
            NgườiDùng.ghi("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (NgườiDùng.sốLượngCácĐốiSố() != 1) { NgườiDùng.ghi("Usage: javac FILE.java\n"); return 2; }
        int cỡTên = CôngCụJava.tên(vănBảnTênTệp, NgườiDùng.cácĐốiSố(0));
        if (cỡTên < 6 || cỡTên > 62 || vănBảnTênTệp[cỡTên - 5] != '.' || vănBảnTênTệp[cỡTên - 4] != 'j'
            || vănBảnTênTệp[cỡTên - 3] != 'a' || vănBảnTênTệp[cỡTên - 2] != 'v' || vănBảnTênTệp[cỡTên - 1] != 'a') {
            NgườiDùng.ghi("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        cỡNguồn = NgườiDùng.đọcTệp(vănBảnTênTệp, mãNguồn);
        if (cỡNguồn < 0) { NgườiDùng.ghi("javac: cannot read source: "); CôngCụJava.ghiSố(cỡNguồn); NgườiDùng.ghiGiáTrịKýTự(10); return 1; }
        cỡNguồn = CôngCụJava.giảiMãNguồn(mãNguồn, cỡNguồn);
        if (cỡNguồn < 0) { NgườiDùng.ghi("javac error: invalid UTF-8 source\n"); return 1; }
        giáTrịCắt(); if (!lỗi) đọcKhaiBáo();
        if (!lỗi) {
            if (độDàiTừTố[từTốLớp] != cỡTên - 5) giáTrịSựThấtBại("class name must match file name");
            for (int trịSố = 0; trịSố < cỡTên - 5; trịSố++) if (mãNguồn[vịTríTừTố[từTốLớp] + trịSố] != vănBảnTênTệp[trịSố]) giáTrịSựThấtBại("class name must match file name");
        }
        for (phươngThứcHiệnTại = 0; phươngThứcHiệnTại < sốLượngPhươngThức && !lỗi; phươngThứcHiệnTại++) {
            vịTrí = thânPhươngThức[phươngThứcHiệnTại]; mãPhươngThức[phươngThứcHiệnTại] = cỡMã; sốLượngCụcBộ = 0; giáTrịĐộSâu = 0;
            for (int trịSố = 0; trịSố < sốLượngĐốiSốPhươngThức[phươngThứcHiệnTại]; trịSố++) thêmCụcBộ(tênĐốiSốPhươngThức[phươngThứcHiệnTại * 16 + trịSố], kiểuĐốiSốPhươngThức[phươngThứcHiệnTại * 16 + trịSố]);
            boolean kếtQuảTrảVề = giáTrịCâuLệnh();
            if (!kếtQuảTrảVề && trảVềPhươngThức[phươngThứcHiệnTại] != 0) giáTrịSựThấtBại("missing return");
            // Điểm hợp sau nhánh phải là một lệnh thực sự, theo bộ kiểm chứng phiên bản 49.
            if (trảVềPhươngThức[phươngThứcHiệnTại] == 0) phátGiáTrị(177);
            else { boolean SốNguyên = trảVềPhươngThức[phươngThứcHiệnTại] <= 2 || trảVềPhươngThức[phươngThứcHiệnTại] == 5; phátGiáTrị(SốNguyên ? 3 : 1); phátGiáTrị(SốNguyên ? 172 : 176); }
            if (vịTrí != kếtThúcPhươngThức[phươngThứcHiệnTại]) giáTrịSựThấtBại("invalid method body");
            cácBiếnCụcBộPhươngThức[phươngThứcHiệnTại] = sốLượngCụcBộ; độDàiPhươngThức[phươngThứcHiệnTại] = cỡMã - mãPhươngThức[phươngThứcHiệnTại];
        }
        if (lỗi) return 1;
        ghiLớp(); if (lỗi) return 1;
        vănBảnTênTệp[cỡTên - 4] = 'c'; vănBảnTênTệp[cỡTên - 3] = 'l'; vănBảnTênTệp[cỡTên - 2] = 'a';
        vănBảnTênTệp[cỡTên - 1] = 's'; vănBảnTênTệp[cỡTên] = 's'; vănBảnTênTệp[cỡTên + 1] = 0;
        int kếtQuả = NgườiDùng.ghiTệp(vănBảnTênTệp, ĐầuRa, cỡĐầuRa);
        if (kếtQuả < 0) { NgườiDùng.ghi("javac: cannot save class: "); CôngCụJava.ghiSố(kếtQuả); NgườiDùng.ghiGiáTrịKýTự(10); return 1; }
        NgườiDùng.ghi("Compiled: "); for (int trịSố = 0; vănBảnTênTệp[trịSố] != 0; trịSố++) NgườiDùng.ghiGiáTrịKýTự(vănBảnTênTệp[trịSố]);
        NgườiDùng.ghi(" (JVM class version 49)\n"); return 0;
    }
}
