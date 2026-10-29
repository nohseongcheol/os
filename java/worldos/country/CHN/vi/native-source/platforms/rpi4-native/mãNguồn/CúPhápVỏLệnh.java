// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Cú pháp tương tác có giới hạn. Các ống chạy tuần tự; môi trường được chia sẻ trong cùng một trình thông dịch lệnh. */
public final class CúPhápVỏLệnh {
    static int[] mãNguồn = new int[4 * 4096], giáTrịLoại = new int[4 * 128], chạy = new int[4 * 128], phầnKết = new int[4 * 128];
    static int[] tênBiến = new int[16 * 32], dữLiệuBiến = new int[16 * 256], độDàiTên = new int[16], độDàiGiáTrị = new int[16];
    static int[] giáTrịKịchBản = new int[4 * 16384];
    static int giáTrịTrạngThái, giáTrịĐộSâu, đãGhiXong;
    static boolean làĐangKếtNối, kếtThúcKịchBản, lỗiPhầnMởRộng;
    static boolean kýTựTên(int mãKýTự) { return mãKýTự >= 'a' && mãKýTự <= 'z' || mãKýTự >= 'A' && mãKýTự <= 'Z' || mãKýTự == '_' || mãKýTự >= 128; }
    static boolean hậuTốTên(int mãKýTự) { return kýTựTên(mãKýTự) || mãKýTự >= '0' && mãKýTự <= '9'; }
    static void lỗi(String vănBản) { BoMạch.vàoRaChuyển(0); VàoRaThiếtBịCuối.ghi("lệnh phânTíchCúPhápGiáTrị: "); VàoRaThiếtBịCuối.ghi(vănBản); VàoRaThiếtBịCuối.KýTự(10); giáTrịTrạngThái = 2; }
    static int đọc(int sốLượngMục, int độSâu) {
        int chỉSốHiệnTại = 0, sốLượngTổngCộng = 0, vịTríCơSở = độSâu * 4096, kýTựĐặcBiệt = độSâu * 128;
        while (chỉSốHiệnTại < sốLượngMục) {
            while (chỉSốHiệnTại < sốLượngMục && (mãNguồn[vịTríCơSở + chỉSốHiệnTại] == 32 || mãNguồn[vịTríCơSở + chỉSốHiệnTại] == 9)) chỉSốHiệnTại++;
            if (chỉSốHiệnTại == sốLượngMục || mãNguồn[vịTríCơSở + chỉSốHiệnTại] == '#') break;
            if (sốLượngTổngCộng == 128) { lỗi("낱말이 너무 많습니다"); return -1; }
            int bắtChạyVịTrí = chỉSốHiệnTại, mãKýTự = mãNguồn[vịTríCơSở + chỉSốHiệnTại], loạiDữLiệu = 0;
            if (mãKýTự == ';') { loạiDữLiệu = 1; chỉSốHiệnTại++; }
            else if (mãKýTự == '&') { if (chỉSốHiệnTại + 1 >= sốLượngMục || mãNguồn[vịTríCơSở + chỉSốHiệnTại + 1] != '&') { lỗi("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } loạiDữLiệu = 2; chỉSốHiệnTại += 2; }
            else if (mãKýTự == '|') { chỉSốHiệnTại++; loạiDữLiệu = chỉSốHiệnTại < sốLượngMục && mãNguồn[vịTríCơSở + chỉSốHiệnTại] == '|' ? 3 : 4; if (loạiDữLiệu == 3) chỉSốHiệnTại++; }
            else if (mãKýTự == '>') { chỉSốHiệnTại++; loạiDữLiệu = chỉSốHiệnTại < sốLượngMục && mãNguồn[vịTríCơSở + chỉSốHiệnTại] == '>' ? 6 : 5; if (loạiDữLiệu == 6) chỉSốHiệnTại++; }
            else if (mãKýTự == '<') { loạiDữLiệu = 7; chỉSốHiệnTại++; }
            else {
                int dấuTrích = 0;
                while (chỉSốHiệnTại < sốLượngMục) {
                    mãKýTự = mãNguồn[vịTríCơSở + chỉSốHiệnTại];
                    if (mãKýTự == '`' && dấuTrích != 39 || mãKýTự == '$' && dấuTrích != 39 && chỉSốHiệnTại + 1 < sốLượngMục && mãNguồn[vịTríCơSở + chỉSốHiệnTại + 1] == '(') { lỗi("lệnh kếtQuả 치환은 지원하지 않습니다"); return -1; }
                    if (mãKýTự == '\\' && dấuTrích != 39) { if (++chỉSốHiệnTại == sốLượngMục) { lỗi("dòng 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } chỉSốHiệnTại++; continue; }
                    if (mãKýTự == dấuTrích) { dấuTrích = 0; chỉSốHiệnTại++; continue; }
                    if (dấuTrích == 0 && (mãKýTự == 39 || mãKýTự == 34)) { dấuTrích = mãKýTự; chỉSốHiệnTại++; continue; }
                    if (dấuTrích == 0 && (mãKýTự == 32 || mãKýTự == 9 || mãKýTự == ';' || mãKýTự == '&' || mãKýTự == '|' || mãKýTự == '<' || mãKýTự == '>')) break;
                    chỉSốHiệnTại++;
                }
                if (dấuTrích != 0) { lỗi("따옴표가 닫히지 않았습니다"); return -1; }
                if (chỉSốHiệnTại < sốLượngMục && (mãNguồn[vịTríCơSở + chỉSốHiệnTại] == '>' || mãNguồn[vịTríCơSở + chỉSốHiệnTại] == '<')) {
                    boolean giáTrịThuộcSố = chỉSốHiệnTại > bắtChạyVịTrí;
                    for (int chỉSốVòngLặp = bắtChạyVịTrí; chỉSốVòngLặp < chỉSốHiệnTại; chỉSốVòngLặp++) if (mãNguồn[vịTríCơSở + chỉSốVòngLặp] < '0' || mãNguồn[vịTríCơSở + chỉSốVòngLặp] > '9') giáTrịThuộcSố = false;
                    if (giáTrịThuộcSố) { lỗi("번호를 지정한 Tệp mụcBộMôTả đầuRaĐầuVào 전환은 지원하지 않습니다"); return -1; }
                }
            }
            giáTrịLoại[kýTựĐặcBiệt + sốLượngTổngCộng] = loạiDữLiệu; chạy[kýTựĐặcBiệt + sốLượngTổngCộng] = bắtChạyVịTrí; phầnKết[kýTựĐặcBiệt + sốLượngTổngCộng] = chỉSốHiệnTại; sốLượngTổngCộng++;
        }
        boolean từTừVựng = false;
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < sốLượngTổngCộng; chỉSốVòngLặp++) {
            int dữLiệuTạm = giáTrịLoại[kýTựĐặcBiệt + chỉSốVòngLặp];
            if (dữLiệuTạm == 0) từTừVựng = true;
            else if (dữLiệuTạm >= 5) { if (++chỉSốVòngLặp == sốLượngTổngCộng || giáTrịLoại[kýTựĐặcBiệt + chỉSốVòngLặp] != 0) { lỗi("đầuRaĐầuVào 전환에 Tệp 이름이 필요합니다"); return -1; } }
            else { if (!từTừVựng || chỉSốVòngLặp == sốLượngTổngCộng - 1 && dữLiệuTạm != 1) { lỗi("명령이 빠졌습니다"); return -1; } từTừVựng = false; }
        }
        if (sốLượngTổngCộng > 0 && !từTừVựng && giáTrịLoại[kýTựĐặcBiệt + sốLượngTổngCộng - 1] != 1) { lỗi("명령이 빠졌습니다"); return -1; }
        return sốLượngTổngCộng;
    }
    static boolean vănBảnKhoảng(int[] mảngDữLiệu, int bắtChạyCụcBộ, int sốLượngMục, String vịTríKýTự) {
        if (sốLượngMục != vịTríKýTự.length()) return false; for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < sốLượngMục; chỉSốVòngLặp++) if (mảngDữLiệu[bắtChạyCụcBộ + chỉSốVòngLặp] != vịTríKýTự.charAt(chỉSốVòngLặp)) return false; return true;
    }
    static void đặtGiáTrị(int dữLiệuByte) {
        if (đãGhiXong >= TrìnhThôngDịchLệnh.giáTrịTừTố.length) { if (!lỗiPhầnMởRộng) lỗi("변수를 펼친 명령이 너무 깁니다"); lỗiPhầnMởRộng = true; return; }
        TrìnhThôngDịchLệnh.giáTrịTừTố[đãGhiXong++] = dữLiệuByte;
    }
    static void giáTrịBiến(int[] mảngDữLiệu, int bắtChạyVịTrí, int sốLượngMục) {
        if (vănBảnKhoảng(mảngDữLiệu, bắtChạyVịTrí, sốLượngMục, "PWD")) { đặtGiáTrị('/'); for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < CácTệpBộNhớ.độDàiHiệnTại; chỉSốVòngLặp++) đặtGiáTrị(CácTệpBộNhớ.phầnMụcHiệnTại[chỉSốVòngLặp]); return; }
        if (vănBảnKhoảng(mảngDữLiệu, bắtChạyVịTrí, sốLượngMục, "HOME")) { đặtGiáTrị('/'); return; }
        if (vănBảnKhoảng(mảngDữLiệu, bắtChạyVịTrí, sốLượngMục, "?")) {
            int giáTrịDữLiệu = giáTrịTrạngThái, chữSố = 100; boolean cóĐãBắtChạy = false;
            while (chữSố > 0) { int giáTrịỞCuối = giáTrịDữLiệu / chữSố; if (giáTrịỞCuối != 0 || cóĐãBắtChạy || chữSố == 1) { đặtGiáTrị('0' + giáTrịỞCuối); cóĐãBắtChạy = true; } giáTrịDữLiệu %= chữSố; chữSố /= 10; } return;
        }
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < 16; chỉSốVòngLặp++) if (độDàiTên[chỉSốVòngLặp] == sốLượngMục) {
            boolean cóKhớp = true; for (int vịTríPhíaTrong = 0; vịTríPhíaTrong < sốLượngMục; vịTríPhíaTrong++) if (tênBiến[chỉSốVòngLặp * 32 + vịTríPhíaTrong] != mảngDữLiệu[bắtChạyVịTrí + vịTríPhíaTrong]) cóKhớp = false;
            if (cóKhớp) { for (int vịTríPhíaTrong = 0; vịTríPhíaTrong < độDàiGiáTrị[chỉSốVòngLặp]; vịTríPhíaTrong++) đặtGiáTrị(dữLiệuBiến[chỉSốVòngLặp * 256 + vịTríPhíaTrong]); return; }
        }
    }
    static boolean giáTrịTừ(int chỉSốTừTừVựng, int độSâu) {
        int đọcConTrỏVănBản = chạy[độSâu * 128 + chỉSốTừTừVựng], vịTríKếtThúc = phầnKết[độSâu * 128 + chỉSốTừTừVựng], vịTríCơSở = độSâu * 4096, dấuTrích = 0;
        if (đọcConTrỏVănBản < vịTríKếtThúc && mãNguồn[vịTríCơSở + đọcConTrỏVănBản] == '~' && (đọcConTrỏVănBản + 1 == vịTríKếtThúc || mãNguồn[vịTríCơSở + đọcConTrỏVănBản + 1] == '/')) { đặtGiáTrị('/'); đọcConTrỏVănBản++; }
        while (đọcConTrỏVănBản < vịTríKếtThúc) {
            int mãKýTự = mãNguồn[vịTríCơSở + đọcConTrỏVănBản++];
            if (mãKýTự == dấuTrích) { dấuTrích = 0; continue; }
            if (dấuTrích == 0 && (mãKýTự == 39 || mãKýTự == 34)) { dấuTrích = mãKýTự; continue; }
            if (mãKýTự == '\\' && dấuTrích != 39) { int vịTríKếTiếp = mãNguồn[vịTríCơSở + đọcConTrỏVănBản++]; if (dấuTrích == 34 && vịTríKếTiếp != '$' && vịTríKếTiếp != '"' && vịTríKếTiếp != '\\') đặtGiáTrị('\\'); đặtGiáTrị(vịTríKếTiếp); continue; }
            if (mãKýTự == '$' && dấuTrích != 39 && đọcConTrỏVănBản < vịTríKếtThúc) {
                boolean ngoặcNhọn = mãNguồn[vịTríCơSở + đọcConTrỏVănBản] == '{'; if (ngoặcNhọn) đọcConTrỏVănBản++;
                int bắtĐầu = đọcConTrỏVănBản;
                if (đọcConTrỏVănBản < vịTríKếtThúc && mãNguồn[vịTríCơSở + đọcConTrỏVănBản] == '?') đọcConTrỏVănBản++;
                else while (đọcConTrỏVănBản < vịTríKếtThúc && hậuTốTên(mãNguồn[vịTríCơSở + đọcConTrỏVănBản])) đọcConTrỏVănBản++;
                if (ngoặcNhọn && (đọcConTrỏVănBản == vịTríKếtThúc || mãNguồn[vịTríCơSở + đọcConTrỏVănBản] != '}')) { lỗi("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (đọcConTrỏVănBản == bắtĐầu && !ngoặcNhọn) { đặtGiáTrị('$'); continue; }
                giáTrịBiến(mãNguồn, vịTríCơSở + bắtĐầu, đọcConTrỏVănBản - bắtĐầu); if (ngoặcNhọn) đọcConTrỏVănBản++; continue;
            }
            đặtGiáTrị(mãKýTự);
        }
        return !lỗiPhầnMởRộng;
    }
    static int cácThiếtLậpMôiTrường(int chỉSốĐốiSố, boolean gỡ) {
        int bắtChạyCụcBộ = TrìnhThôngDịchLệnh.điểmĐangBắtChạy[chỉSốĐốiSố], vịTríKếtThúc = bắtChạyCụcBộ + TrìnhThôngDịchLệnh.độDài[chỉSốĐốiSố], vịTríTínhBằngNhau = bắtChạyCụcBộ;
        while (vịTríTínhBằngNhau < vịTríKếtThúc && TrìnhThôngDịchLệnh.giáTrịTừTố[vịTríTínhBằngNhau] != '=') vịTríTínhBằngNhau++;
        int sốLượngMục = vịTríTínhBằngNhau - bắtChạyCụcBộ;
        if (sốLượngMục < 1 || sốLượngMục > 31 || !kýTựTên(TrìnhThôngDịchLệnh.giáTrịTừTố[bắtChạyCụcBộ]) || !gỡ && vịTríTínhBằngNhau == vịTríKếtThúc || vịTríKếtThúc - vịTríTínhBằngNhau - 1 > 255) return 2;
        for (int chỉSốVòngLặp = bắtChạyCụcBộ; chỉSốVòngLặp < vịTríTínhBằngNhau; chỉSốVòngLặp++) if (!hậuTốTên(TrìnhThôngDịchLệnh.giáTrịTừTố[chỉSốVòngLặp])) return 2;
        if (vănBảnKhoảng(TrìnhThôngDịchLệnh.giáTrịTừTố, bắtChạyCụcBộ, sốLượngMục, "PWD") || vănBảnKhoảng(TrìnhThôngDịchLệnh.giáTrịTừTố, bắtChạyCụcBộ, sốLượngMục, "HOME")) return 2;
        int đãTìmThấyĐãLà = -1, làTrạngTháiRỗng = -1;
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < 16; chỉSốVòngLặp++) {
            if (độDàiTên[chỉSốVòngLặp] == 0) làTrạngTháiRỗng = chỉSốVòngLặp;
            if (độDàiTên[chỉSốVòngLặp] != sốLượngMục) continue;
            boolean cóKhớp = true; for (int vịTríPhíaTrong = 0; vịTríPhíaTrong < sốLượngMục; vịTríPhíaTrong++) if (tênBiến[chỉSốVòngLặp * 32 + vịTríPhíaTrong] != TrìnhThôngDịchLệnh.giáTrịTừTố[bắtChạyCụcBộ + vịTríPhíaTrong]) cóKhớp = false;
            if (cóKhớp) đãTìmThấyĐãLà = chỉSốVòngLặp;
        }
        if (gỡ) { if (đãTìmThấyĐãLà >= 0) độDàiTên[đãTìmThấyĐãLà] = 0; return 0; }
        if (đãTìmThấyĐãLà < 0) đãTìmThấyĐãLà = làTrạngTháiRỗng; if (đãTìmThấyĐãLà < 0) return 1;
        độDàiTên[đãTìmThấyĐãLà] = sốLượngMục; độDàiGiáTrị[đãTìmThấyĐãLà] = vịTríKếtThúc - vịTríTínhBằngNhau - 1;
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < sốLượngMục; chỉSốVòngLặp++) tênBiến[đãTìmThấyĐãLà * 32 + chỉSốVòngLặp] = TrìnhThôngDịchLệnh.giáTrịTừTố[bắtChạyCụcBộ + chỉSốVòngLặp];
        for (int chỉSốVòngLặp = vịTríTínhBằngNhau + 1; chỉSốVòngLặp < vịTríKếtThúc; chỉSốVòngLặp++) dữLiệuBiến[đãTìmThấyĐãLà * 256 + chỉSốVòngLặp - vịTríTínhBằngNhau - 1] = TrìnhThôngDịchLệnh.giáTrịTừTố[chỉSốVòngLặp];
        return 0;
    }
    static void hiệnMôiTrường() {
        VàoRaThiếtBịCuối.ghi("HOME=/\nPWD="); CácTệpBộNhớ.ghiHiệnTại(); VàoRaThiếtBịCuối.KýTự(10);
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < 16; chỉSốVòngLặp++) if (độDàiTên[chỉSốVòngLặp] > 0) {
            for (int vịTríPhíaTrong = 0; vịTríPhíaTrong < độDàiTên[chỉSốVòngLặp]; vịTríPhíaTrong++) BoMạch.ghiNốiTiếp(tênBiến[chỉSốVòngLặp * 32 + vịTríPhíaTrong]); VàoRaThiếtBịCuối.KýTự('=');
            for (int vịTríPhíaTrong = 0; vịTríPhíaTrong < độDàiGiáTrị[chỉSốVòngLặp]; vịTríPhíaTrong++) BoMạch.ghiNốiTiếp(dữLiệuBiến[chỉSốVòngLặp * 256 + vịTríPhíaTrong]); VàoRaThiếtBịCuối.KýTự(10);
        }
    }
    static void thựcThiLệnh(int[] mảngDữLiệu, int bắtChạyĐộDời, int sốLượngMục, int độSâu) {
        if (độSâu >= 4 || sốLượngMục > 4096) { lỗi("lệnh 파일의 giáTrịLồngNhau 또는 dòng độDài 제한을 넘었습니다"); return; }
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < sốLượngMục; chỉSốVòngLặp++) mãNguồn[độSâu * 4096 + chỉSốVòngLặp] = mảngDữLiệu[bắtChạyĐộDời + chỉSốVòngLặp];
        int sốLượngTổngCộng = đọc(sốLượngMục, độSâu); if (sốLượngTổngCộng < 0) return;
        int đọcConTrỏVănBản = 0, đãĐápỨngĐiềuKiện = 1;
        while (đọcConTrỏVănBản < sốLượngTổngCộng) {
            int kếtThúcNhóm = đọcConTrỏVănBản;
            while (kếtThúcNhóm < sốLượngTổngCộng && (giáTrịLoại[độSâu * 128 + kếtThúcNhóm] == 0 || giáTrịLoại[độSâu * 128 + kếtThúcNhóm] >= 4)) kếtThúcNhóm++;
            boolean thựcThi = đãĐápỨngĐiềuKiện == 1 || đãĐápỨngĐiềuKiện == 2 && giáTrịTrạngThái == 0 || đãĐápỨngĐiềuKiện == 3 && giáTrịTrạngThái != 0;
            if (thựcThi) {
                boolean chỉSốPhầnMụcTrướcĐó = false;
                while (đọcConTrỏVănBản < kếtThúcNhóm) {
                    int vịTríKếTiếp = đọcConTrỏVănBản; while (vịTríKếTiếp < kếtThúcNhóm && giáTrịLoại[độSâu * 128 + vịTríKếTiếp] != 4) vịTríKếTiếp++;
                    boolean kếtNốiLuồng = vịTríKếTiếp < kếtThúcNhóm; int trangĐầuVào = -1, trangĐầuRa = -1, chếĐộRaNgoài = 0;
                    TrìnhThôngDịchLệnh.sốLượngTừTố = 0; đãGhiXong = 0; lỗiPhầnMởRộng = false;
                    for (int chỉSốVòngLặp = đọcConTrỏVănBản; chỉSốVòngLặp < vịTríKếTiếp; chỉSốVòngLặp++) {
                        int loạiDữLiệu = giáTrịLoại[độSâu * 128 + chỉSốVòngLặp];
                        if (loạiDữLiệu >= 5) { if (loạiDữLiệu == 7) { if (trangĐầuVào >= 0) { lỗi("giáTrịVào 전환이 겹쳤습니다"); return; } trangĐầuVào = ++chỉSốVòngLặp; } else { if (trangĐầuRa >= 0) { lỗi("ĐầuRa 전환이 겹쳤습니다"); return; } trangĐầuRa = ++chỉSốVòngLặp; chếĐộRaNgoài = loạiDữLiệu; } continue; }
                        if (TrìnhThôngDịchLệnh.sốLượngTừTố == 32) { lỗi("인수가 너무 많습니다"); return; }
                        int chỉSốĐốiSố = TrìnhThôngDịchLệnh.sốLượngTừTố++; TrìnhThôngDịchLệnh.điểmĐangBắtChạy[chỉSốĐốiSố] = đãGhiXong;
                        if (!giáTrịTừ(chỉSốVòngLặp, độSâu)) return;
                        TrìnhThôngDịchLệnh.độDài[chỉSốĐốiSố] = đãGhiXong - TrìnhThôngDịchLệnh.điểmĐangBắtChạy[chỉSốĐốiSố];
                    }
                    làĐangKếtNối = chỉSốPhầnMụcTrướcĐó || kếtNốiLuồng || trangĐầuVào >= 0 || trangĐầuRa >= 0;
                    if (làĐangKếtNối && (TrìnhThôngDịchLệnh.vănBảnBằng(0, "vi") || TrìnhThôngDịchLệnh.vănBảnBằng(0, "edit") || TrìnhThôngDịchLệnh.vănBảnBằng(0, "load") || TrìnhThôngDịchLệnh.vănBảnBằng(0, "gui") || TrìnhThôngDịchLệnh.vănBảnBằng(0, "terminal") || TrìnhThôngDịchLệnh.vănBảnBằng(0, "sh") || TrìnhThôngDịchLệnh.vănBảnBằng(0, "source"))) { lỗi("tươngTác 명령과 lệnh 파일은 đầuRaĐầuVào 전환이나 giáTrịLuồng 연결에 쓸 trịSố 없습니다"); return; }
                    VàoRaVỏLệnh.chạy(chỉSốPhầnMụcTrướcĐó, kếtNốiLuồng);
                    for (int đổiHướngGọn = 0; đổiHướngGọn < 2; đổiHướngGọn++) {
                        int vịTríMục = đổiHướngGọn == 0 ? trangĐầuVào : trangĐầuRa; if (vịTríMục < 0) continue;
                        int bắtChạyVịTrí = đãGhiXong; if (!giáTrịTừ(vịTríMục, độSâu)) { VàoRaVỏLệnh.phầnKết(); return; }
                        int giáTrịĐãXửLý = CácTệpBộNhớ.bắtChạyĐườngDẫn(đãGhiXong - bắtChạyVịTrí);
                        for (int vịTríPhíaTrong = bắtChạyVịTrí; giáTrịĐãXửLý >= 0 && vịTríPhíaTrong < đãGhiXong; vịTríPhíaTrong++) giáTrịĐãXửLý = CácTệpBộNhớ.byteĐườngDẫn(vịTríPhíaTrong - bắtChạyVịTrí, TrìnhThôngDịchLệnh.giáTrịTừTố[vịTríPhíaTrong]);
                        if (giáTrịĐãXửLý >= 0) giáTrịĐãXửLý = CácTệpBộNhớ.mở(đổiHướngGọn == 0 ? 0 : chếĐộRaNgoài == 6 ? 1089 : 577);
                        if (giáTrịĐãXửLý < 0) { VàoRaVỏLệnh.phầnKết(); TrìnhThôngDịchLệnh.lỗi(giáTrịĐãXửLý); giáTrịTrạngThái = 1; return; }
                        if (đổiHướngGọn == 0) VàoRaVỏLệnh.tệpĐầuVào = giáTrịĐãXửLý; else VàoRaVỏLệnh.tệpĐầuRa = giáTrịĐãXửLý;
                    }
                    VàoRaVỏLệnh.choPhépTươngTác = độSâu == 0 && đọcConTrỏVănBản == 0 && vịTríKếTiếp == sốLượngTổngCộng;
                    giáTrịĐộSâu = độSâu; TrìnhThôngDịchLệnh.kếtQuả = 0; BoMạch.vàoRaChuyển(1);
                    TrìnhThôngDịchLệnh.lệnh();
                    BoMạch.thiếtBịCuối(3);
                    int giáTrịĐãTrảVề = TrìnhThôngDịchLệnh.kếtQuả, lỗiLuồng = VàoRaVỏLệnh.giáTrịSựThấtBại;
                    VàoRaVỏLệnh.phầnKết(); làĐangKếtNối = false;
                    giáTrịTrạngThái = lỗiLuồng < 0 ? 1 : giáTrịĐãTrảVề;
                    if (lỗiLuồng < 0) { TrìnhThôngDịchLệnh.lỗi(lỗiLuồng); return; }
                    if (kếtThúcKịchBản || giáTrịĐãTrảVề == -1005) return;
                    chỉSốPhầnMụcTrướcĐó = true; đọcConTrỏVănBản = vịTríKếTiếp + 1;
                }
            }
            if (kếtThúcNhóm < sốLượngTổngCộng) đãĐápỨngĐiềuKiện = giáTrịLoại[độSâu * 128 + kếtThúcNhóm];
            đọcConTrỏVănBản = kếtThúcNhóm + 1;
        }
    }
    static void thựcThiTệp() {
        if (TrìnhThôngDịchLệnh.sốLượngTừTố != 2 || giáTrịĐộSâu >= 3) { TrìnhThôngDịchLệnh.kếtQuả = 2; VàoRaThiếtBịCuối.ghi("사용법: sh Tệp (giáTrịLồngNhau giáTrịĐộSâu <= 3)\n"); return; }
        int độSâu = giáTrịĐộSâu + 1, giáTrịĐãXửLý = TrìnhThôngDịchLệnh.đườngDẫn(1); if (giáTrịĐãXửLý >= 0) giáTrịĐãXửLý = CácTệpBộNhớ.mở(0);
        if (giáTrịĐãXửLý < 0) { TrìnhThôngDịchLệnh.lỗi(giáTrịĐãXửLý); return; }
        int sốLượngMục = 0, dữLiệuByte;
        while ((dữLiệuByte = CácTệpBộNhớ.đọc(giáTrịĐãXửLý)) != 256 && dữLiệuByte >= 0 && sốLượngMục < 16384) giáTrịKịchBản[độSâu * 16384 + sốLượngMục++] = dữLiệuByte;
        CácTệpBộNhớ.đóng(giáTrịĐãXửLý); BoMạch.vàoRaChuyển(0);
        for (int đọcConTrỏVănBản = 0; đọcConTrỏVănBản < sốLượngMục && !kếtThúcKịchBản;) {
            int vịTríKếtThúc = đọcConTrỏVănBản; while (vịTríKếtThúc < sốLượngMục && giáTrịKịchBản[độSâu * 16384 + vịTríKếtThúc] != 10) vịTríKếtThúc++;
            int độDàiHợpLệ = vịTríKếtThúc - đọcConTrỏVănBản; if (độDàiHợpLệ > 0 && giáTrịKịchBản[độSâu * 16384 + vịTríKếtThúc - 1] == 13) độDàiHợpLệ--;
            thựcThiLệnh(giáTrịKịchBản, độSâu * 16384 + đọcConTrỏVănBản, độDàiHợpLệ, độSâu); đọcConTrỏVănBản = vịTríKếtThúc + 1;
        }
        TrìnhThôngDịchLệnh.kếtQuả = giáTrịTrạngThái; kếtThúcKịchBản = false; giáTrịĐộSâu = độSâu - 1;
    }
}
