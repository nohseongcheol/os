// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Dòng lệnh UTF-8 qua UART, hỗ trợ dấu trích dẫn, Backspace, Ctrl-U, Ctrl-C và trình soạn thảo trong RAM. */
public final class TrìnhThôngDịchLệnh {
    static int[] dòng = new int[4096], giáTrịTừTố = new int[4096], điểmĐangBắtChạy = new int[32], độDài = new int[32];
    static int[] cácNộiDungĐãSửa = new int[16384], tênSửa = new int[63];
    static int sốLượngTừTố, độDàiTênSửa, kếtQuả;
    static boolean dòngTrướcĐó;
    static void byteNguyênBản(int giáTrị) { BoMạch.ghiNốiTiếp(giáTrị); }
    static int đọcDòngĐầuVào() { return TrìnhSoạnThảoDòng.đọc(); }
    static boolean cácGiáTrịChia(int cỡ) {
        int vịTrí = 0, phầnKết = 0; sốLượngTừTố = 0;
        while (vịTrí < cỡ) {
            while (vịTrí < cỡ && (dòng[vịTrí] == 32 || dòng[vịTrí] == 9)) vịTrí++;
            if (vịTrí == cỡ) break;
            if (sốLượngTừTố == 16) { VàoRaThiếtBịCuối.ghi("lệnh phânTíchCúPhápGiáTrị: 인수가 너무 많습니다\n"); return false; }
            điểmĐangBắtChạy[sốLượngTừTố] = phầnKết; int giáTrịDấuTrích = 0;
            while (vịTrí < cỡ) {
                int giáTrị = dòng[vịTrí++];
                if (giáTrịDấuTrích == 0 && (giáTrị == 32 || giáTrị == 9)) break;
                if (giáTrị == giáTrịDấuTrích) { giáTrịDấuTrích = 0; continue; }
                if (giáTrịDấuTrích == 0 && (giáTrị == 39 || giáTrị == 34)) { giáTrịDấuTrích = giáTrị; continue; }
                giáTrịTừTố[phầnKết++] = giáTrị;
            }
            if (giáTrịDấuTrích != 0) { VàoRaThiếtBịCuối.ghi("lệnh phânTíchCúPhápGiáTrị: 따옴표가 닫히지 않았습니다\n"); return false; }
            độDài[sốLượngTừTố] = phầnKết - điểmĐangBắtChạy[sốLượngTừTố]; sốLượngTừTố++;
        }
        return true;
    }
    static boolean vănBảnBằng(int sốHiệu, String vănBảnTừ) {
        if (sốHiệu >= sốLượngTừTố) return false;
        int chỉSốVịTrí=0;
        for (int chỉSốThứBậc=0; chỉSốThứBậc<vănBảnTừ.length(); chỉSốThứBậc++) {
            int mãKýTự=vănBảnTừ.charAt(chỉSốThứBậc);
            if (mãKýTự>=0xd800 && mãKýTự<=0xdbff && chỉSốThứBậc+1<vănBảnTừ.length()) mãKýTự=0x10000+((mãKýTự-0xd800)<<10)+vănBảnTừ.charAt(++chỉSốThứBậc)-0xdc00;
            int sốLượngByte=mãKýTự<128?1:mãKýTự<2048?2:mãKýTự<65536?3:4;
            for (int giáTrịDãy=sốLượngByte-1; giáTrịDãy>=0; giáTrịDãy--) {
                int giáTrị=sốLượngByte==1?mãKýTự:giáTrịDãy==sốLượngByte-1?(sốLượngByte==2?0xc0:sốLượngByte==3?0xe0:0xf0)|(mãKýTự>>(6*giáTrịDãy)):0x80|((mãKýTự>>(6*giáTrịDãy))&63);
                if (chỉSốVịTrí>=độDài[sốHiệu] || giáTrịTừTố[điểmĐangBắtChạy[sốHiệu]+chỉSốVịTrí++]!=giáTrị) return false;
            }
        }
        return chỉSốVịTrí==độDài[sốHiệu];
    }
    static int đườngDẫn(int sốHiệu) {
        if (sốHiệu >= sốLượngTừTố) return -22;
        int kếtQuả = CácTệpBộNhớ.bắtChạyĐườngDẫn(độDài[sốHiệu]); if (kếtQuả < 0) return kếtQuả;
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < độDài[sốHiệu]; chỉSốVòngLặp++) {
            kếtQuả = CácTệpBộNhớ.byteĐườngDẫn(chỉSốVòngLặp, giáTrịTừTố[điểmĐangBắtChạy[sốHiệu] + chỉSốVòngLặp]); if (kếtQuả < 0) return kếtQuả;
        }
        return 0;
    }
    static void lỗi(int sốHiệu) { kếtQuả = 1; VàoRaThiếtBịCuối.ghi("lỗi "); VàoRaThiếtBịCuối.trịSố(sốHiệu); VàoRaThiếtBịCuối.KýTự(10); }
    static void giáTrịKhungNhìn() {
        if (sốLượngTừTố != 2) { VàoRaThiếtBịCuối.ghi("사용법: cat Tệp\n"); return; }
        int kếtQuả = đườngDẫn(1); if (kếtQuả < 0) { lỗi(kếtQuả); return; }
        int Tệp = CácTệpBộNhớ.mở(0); if (Tệp < 0) { lỗi(Tệp); return; }
        while (true) { int giáTrị = CácTệpBộNhớ.đọc(Tệp); if (giáTrị == 256) break; if (giáTrị < 0) { lỗi(giáTrị); break; } byteNguyênBản(giáTrị); }
        CácTệpBộNhớ.đóng(Tệp); VàoRaThiếtBịCuối.KýTự(10);
    }
    static void giáTrịSửa() {
        if (sốLượngTừTố != 2) { VàoRaThiếtBịCuối.ghi("사용법: edit Tệp\n"); return; }
        int kếtQuả = đườngDẫn(1); if (kếtQuả < 0) { lỗi(kếtQuả); return; }
        độDàiTênSửa = độDài[1];
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < độDàiTênSửa; chỉSốVòngLặp++) tênSửa[chỉSốVòngLặp] = giáTrịTừTố[điểmĐangBắtChạy[1] + chỉSốVòngLặp];
        VàoRaThiếtBịCuối.ghi("EDIT: Tệp 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(giáTrịTốiĐa 16384바이트)\n");
        int cỡ = 0;
        while (true) {
            VàoRaThiếtBịCuối.ghi("edit> "); int giáTrịVào = đọcDòngĐầuVào();
            if (giáTrịVào < 0) { VàoRaThiếtBịCuối.ghi("EDIT CANCELLED\n"); return; }
            if (giáTrịVào == 1 && dòng[0] == '.') break;
            if (giáTrịVào + 1 > cácNộiDungĐãSửa.length - cỡ) { VàoRaThiếtBịCuối.ghi("EDIT CANCELLED: file too large\n"); return; }
            for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < giáTrịVào; chỉSốVòngLặp++) cácNộiDungĐãSửa[cỡ++] = dòng[chỉSốVòngLặp];
            cácNộiDungĐãSửa[cỡ++] = 10;
        }
        CácTệpBộNhớ.bắtChạyĐườngDẫn(độDàiTênSửa);
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < độDàiTênSửa; chỉSốVòngLặp++) CácTệpBộNhớ.byteĐườngDẫn(chỉSốVòngLặp, tênSửa[chỉSốVòngLặp]);
        int Tệp = CácTệpBộNhớ.mở(577); if (Tệp < 0) { lỗi(Tệp); return; }
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < cỡ; chỉSốVòngLặp++) CácTệpBộNhớ.ghi(Tệp, cácNộiDungĐãSửa[chỉSốVòngLặp]);
        CácTệpBộNhớ.đóng(Tệp); VàoRaThiếtBịCuối.ghi("SAVED "); VàoRaThiếtBịCuối.trịSố(cỡ); VàoRaThiếtBịCuối.ghi("giáTrịByte(주기억 Tệp)\n");
    }
    static int giáTrịThậpLụcPhân(int giáTrị) {
        if (giáTrị >= '0' && giáTrị <= '9') return giáTrị - '0';
        if (giáTrị >= 'a' && giáTrị <= 'f') return giáTrị - 'a' + 10;
        if (giáTrị >= 'A' && giáTrị <= 'F') return giáTrị - 'A' + 10;
        return -1;
    }
    static void vàoRaNhịPhân(boolean đặtGiáTrị) {
        if (sốLượngTừTố != 2) { VàoRaThiếtBịCuối.ghi("사용법: load Tệp | hex Tệp\n"); return; }
        int kếtQuả = đườngDẫn(1); if (kếtQuả < 0) { lỗi(kếtQuả); return; }
        if (!đặtGiáTrị) {
            int Tệp = CácTệpBộNhớ.mở(0); if (Tệp < 0) { lỗi(Tệp); return; }
            VàoRaThiếtBịCuối.ghi("HEX BEGIN "); VàoRaThiếtBịCuối.trịSố(CácTệpBộNhớ.cỡ(Tệp)); VàoRaThiếtBịCuối.KýTự(10);
            int sốLượngMục = 0;
            while (true) {
                int giáTrị = CácTệpBộNhớ.đọc(Tệp); if (giáTrị < 0 || giáTrị == 256) break;
                VàoRaThiếtBịCuối.KýTự("0123456789abcdef".charAt(giáTrị >> 4)); VàoRaThiếtBịCuối.KýTự("0123456789abcdef".charAt(giáTrị & 15));
                if (++sốLượngMục % 32 == 0) VàoRaThiếtBịCuối.KýTự(10);
            }
            if (sốLượngMục % 32 != 0) VàoRaThiếtBịCuối.KýTự(10);
            CácTệpBộNhớ.đóng(Tệp); VàoRaThiếtBịCuối.ghi("HEX END\n"); return;
        }
        độDàiTênSửa = độDài[1];
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < độDàiTênSửa; chỉSốVòngLặp++) tênSửa[chỉSốVòngLặp] = giáTrịTừTố[điểmĐangBắtChạy[1] + chỉSốVòngLặp];
        VàoRaThiếtBịCuối.ghi("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int cỡ = 0;
        while (true) {
            VàoRaThiếtBịCuối.ghi("hex> "); int giáTrịVào = đọcDòngĐầuVào();
            if (giáTrịVào < 0) { VàoRaThiếtBịCuối.ghi("LOAD CANCELLED\n"); return; }
            if (giáTrịVào == 1 && dòng[0] == '.') break;
            int giáTrịPhíaTrước = -1;
            for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < giáTrịVào; chỉSốVòngLặp++) {
                if (dòng[chỉSốVòngLặp] == 32 || dòng[chỉSốVòngLặp] == 9) continue;
                int giáTrị = giáTrịThậpLụcPhân(dòng[chỉSốVòngLặp]);
                if (giáTrị < 0 || cỡ >= cácNộiDungĐãSửa.length) { VàoRaThiếtBịCuối.ghi("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (giáTrịPhíaTrước < 0) giáTrịPhíaTrước = giáTrị; else { cácNộiDungĐãSửa[cỡ++] = giáTrịPhíaTrước * 16 + giáTrị; giáTrịPhíaTrước = -1; }
            }
            if (giáTrịPhíaTrước >= 0) { VàoRaThiếtBịCuối.ghi("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        CácTệpBộNhớ.bắtChạyĐườngDẫn(độDàiTênSửa);
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < độDàiTênSửa; chỉSốVòngLặp++) CácTệpBộNhớ.byteĐườngDẫn(chỉSốVòngLặp, tênSửa[chỉSốVòngLặp]);
        int Tệp = CácTệpBộNhớ.mở(577); if (Tệp < 0) { lỗi(Tệp); return; }
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < cỡ; chỉSốVòngLặp++) CácTệpBộNhớ.ghi(Tệp, cácNộiDungĐãSửa[chỉSốVòngLặp]);
        CácTệpBộNhớ.đóng(Tệp); VàoRaThiếtBịCuối.ghi("LOADED "); VàoRaThiếtBịCuối.trịSố(cỡ); VàoRaThiếtBịCuối.ghi("giáTrịByte(주기억 Tệp)\n");
    }
    static int CôngCụ(int sốHiệu) {
        return MụcCôngCụ(sốHiệu, 1);
    }
    static int MụcCôngCụ(int sốHiệu, int chạy) {
        if (sốLượngTừTố - chạy > 8) return -22;
        BoMạch.chuẩnBịCácĐốiSố(sốLượngTừTố - chạy);
        for (int dữLiệuĐầuTiên = chạy; dữLiệuĐầuTiên < sốLượngTừTố; dữLiệuĐầuTiên++) {
            if (độDài[dữLiệuĐầuTiên] > 255) return -36;
            for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < độDài[dữLiệuĐầuTiên]; chỉSốVòngLặp++) BoMạch.byteĐốiSố(dữLiệuĐầuTiên - chạy, chỉSốVòngLặp, giáTrịTừTố[điểmĐangBắtChạy[dữLiệuĐầuTiên] + chỉSốVòngLặp]);
        }
        return sốHiệu == -2 ? BoMạch.thựcThiTệpLinux() : sốHiệu < 0 ? BoMạch.thựcThiTệpNgườiDùng() : BoMạch.chạyChươngTrìnhNgườiDùng(sốHiệu);
    }
    static int GóiGộpPython() {
        if (sốLượngTừTố > 8) return -22;
        BoMạch.chuẩnBịCácĐốiSố(sốLượngTừTố);
        String đườngDẫn = "/lib/GóiGộp.py";
        // Ghi chuỗi Java vào bộ đệm đối số UTF-8 của trình thông dịch lệnh.
        int chỉSốVịTrí = 0;
        for (int chỉSốThứBậc = 0; chỉSốThứBậc < đườngDẫn.length(); chỉSốThứBậc++) {
            int giáTrịKýTự = đườngDẫn.charAt(chỉSốThứBậc);
            if (giáTrịKýTự < 128) BoMạch.byteĐốiSố(0, chỉSốVịTrí++, giáTrịKýTự);
            else { BoMạch.byteĐốiSố(0, chỉSốVịTrí++, 0xe0 | (giáTrịKýTự >> 12)); BoMạch.byteĐốiSố(0, chỉSốVịTrí++, 0x80 | ((giáTrịKýTự >> 6) & 63)); BoMạch.byteĐốiSố(0, chỉSốVịTrí++, 0x80 | (giáTrịKýTự & 63)); }
        }
        for (int chỉSốThứBậc = 1; chỉSốThứBậc < sốLượngTừTố; chỉSốThứBậc++) {
            if (độDài[chỉSốThứBậc] > 255) return -36;
            for (int giáTrịKýTự = 0; giáTrịKýTự < độDài[chỉSốThứBậc]; giáTrịKýTự++) BoMạch.byteĐốiSố(chỉSốThứBậc, giáTrịKýTự, giáTrịTừTố[điểmĐangBắtChạy[chỉSốThứBậc] + giáTrịKýTự]);
        }
        return BoMạch.chạyChươngTrìnhNgườiDùng(12);
    }
    static int địnhDạngViệcThựcThi() {
        int giáTrịĐãXửLý = đườngDẫn(0); if (giáTrịĐãXửLý < 0) return giáTrịĐãXửLý;
        int Tệp = CácTệpBộNhớ.mở(0); if (Tệp < 0) return Tệp;
        int dữLiệuĐầuTiên = CácTệpBộNhớ.đọc(Tệp), dữLiệuByte = CácTệpBộNhớ.đọc(Tệp), mãKýTự = CácTệpBộNhớ.đọc(Tệp), giáTrịỞCuối = CácTệpBộNhớ.đọc(Tệp);
        CácTệpBộNhớ.đóng(Tệp);
        if (dữLiệuĐầuTiên == 127 && dữLiệuByte == 'E' && mãKýTự == 'L' && giáTrịỞCuối == 'F') return 1;
        if (dữLiệuĐầuTiên == 'P' && dữLiệuByte == 'K' && mãKýTự == 3 && giáTrịỞCuối == 4) return 2;
        return 0;
    }
    static int chạyVíDụ(int sốHiệu, String cácĐốiSố) {
        BoMạch.chuẩnBịCácĐốiSố(1);
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < cácĐốiSố.length(); chỉSốVòngLặp++) BoMạch.byteĐốiSố(0, chỉSốVòngLặp, cácĐốiSố.charAt(chỉSốVòngLặp));
        return BoMạch.chạyChươngTrìnhNgườiDùng(sốHiệu);
    }
    static void byteVănBản(int Tệp, int giáTrị) { CácTệpBộNhớ.ghi(Tệp, giáTrị); }
    static void tệpTĩnh(String tên, String giáTrịNộiDung) {
        // Tên tệp trong gói dùng ASCII; nội dung tệp được lưu bằng UTF-8.
        CácTệpBộNhớ.bắtChạyĐườngDẫn(tên.length());
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < tên.length(); chỉSốVòngLặp++) CácTệpBộNhớ.byteĐườngDẫn(chỉSốVòngLặp, tên.charAt(chỉSốVòngLặp));
        int Tệp = CácTệpBộNhớ.mở(193); if (Tệp < 0) return;
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < giáTrịNộiDung.length(); chỉSốVòngLặp++) {
            int mãKýTự = giáTrịNộiDung.charAt(chỉSốVòngLặp);
            if (mãKýTự >= 0xd800 && mãKýTự <= 0xdbff && chỉSốVòngLặp + 1 < giáTrịNộiDung.length()) mãKýTự = 0x10000 + ((mãKýTự - 0xd800) << 10) + giáTrịNộiDung.charAt(++chỉSốVòngLặp) - 0xdc00;
            if (mãKýTự < 128) byteVănBản(Tệp, mãKýTự);
            else {
                int trịSố = mãKýTự < 2048 ? 2 : mãKýTự < 65536 ? 3 : 4;
                byteVănBản(Tệp, (trịSố == 2 ? 0xc0 : trịSố == 3 ? 0xe0 : 0xf0) | (mãKýTự >> (6 * (trịSố - 1))));
                for (int sốLượngMục = trịSố - 1; sốLượngMục > 0; sốLượngMục--) byteVănBản(Tệp, 0x80 | ((mãKýTự >> (6 * (sốLượngMục - 1))) & 63));
            }
        }
        CácTệpBộNhớ.đóng(Tệp);
    }
    static void trợGiúpHangul() {
        VàoRaThiếtBịCuối.ghi("Nhấn F9 hoặc Shift+Space để chuyển sang nhập tiếng Việt.\n");
        VàoRaThiếtBịCuối.ghi("  [VI] keyboard; [EN] ASCII\n");
        VàoRaThiếtBịCuối.ghi("  ! → Ă\n");
        VàoRaThiếtBịCuối.ghi("  F9: EN ↔ Tiếng Việt | Ctrl+Shift+V: UTF-8\n");
        VàoRaThiếtBịCuối.ghi("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        VàoRaThiếtBịCuối.ghi("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int đườngDẫnVíDụ(String tên) {
        int sốLượngByte = 0;
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < tên.length(); chỉSốVòngLặp++) { int mãKýTự = tên.charAt(chỉSốVòngLặp); if (mãKýTự >= 0xd800 && mãKýTự <= 0xdfff) return -22; sốLượngByte += mãKýTự < 128 ? 1 : mãKýTự < 2048 ? 2 : 3; }
        int giáTrịĐãXửLý = CácTệpBộNhớ.bắtChạyĐườngDẫn(sốLượngByte); if (giáTrịĐãXửLý < 0) return giáTrịĐãXửLý;
        int chỉSốVịTrí = 0;
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < tên.length(); chỉSốVòngLặp++) {
            int mãKýTự = tên.charAt(chỉSốVòngLặp);
            if (mãKýTự < 128) CácTệpBộNhớ.byteĐườngDẫn(chỉSốVịTrí++, mãKýTự);
            else if (mãKýTự < 2048) { CácTệpBộNhớ.byteĐườngDẫn(chỉSốVịTrí++, 0xc0 | (mãKýTự >> 6)); CácTệpBộNhớ.byteĐườngDẫn(chỉSốVịTrí++, 0x80 | (mãKýTự & 63)); }
            else { CácTệpBộNhớ.byteĐườngDẫn(chỉSốVịTrí++, 0xe0 | (mãKýTự >> 12)); CácTệpBộNhớ.byteĐườngDẫn(chỉSốVịTrí++, 0x80 | ((mãKýTự >> 6) & 63)); CácTệpBộNhớ.byteĐườngDẫn(chỉSốVịTrí++, 0x80 | (mãKýTự & 63)); }
        }
        return 0;
    }
    static int thưMụcVíDụ(String tên) {
        int giáTrịĐãXửLý = đườngDẫnVíDụ(tên); if (giáTrịĐãXửLý < 0) return giáTrịĐãXửLý;
        giáTrịĐãXửLý = CácTệpBộNhớ.tạoThưMục(); return giáTrịĐãXửLý == -17 ? 0 : giáTrịĐãXửLý;
    }
    static int tệpVíDụ(String tên, String DữLiệu) {
        int giáTrịĐãXửLý = đườngDẫnVíDụ(tên); if (giáTrịĐãXửLý < 0) return giáTrịĐãXửLý;
        int Tệp = CácTệpBộNhớ.mở(193); if (Tệp == -17) return 0; if (Tệp < 0) return Tệp;
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < DữLiệu.length(); chỉSốVòngLặp += 2) {
            giáTrịĐãXửLý = CácTệpBộNhớ.ghi(Tệp, giáTrịThậpLụcPhân(DữLiệu.charAt(chỉSốVòngLặp)) * 16 + giáTrịThậpLụcPhân(DữLiệu.charAt(chỉSốVòngLặp + 1)));
            if (giáTrịĐãXửLý < 0) { CácTệpBộNhớ.đóng(Tệp); return giáTrịĐãXửLý; }
        }
        return CácTệpBộNhớ.đóng(Tệp);
    }
    static void hiệnTrợGiúp() {
        côngCụHệThống.hiệnTrợGiúp();
        VàoRaThiếtBịCuối.ghi("sshd / vỏLệnhAnToàn start|stop|status: SSH :22 (user, 장치별 giáTrịMậtKhẩu)\n");
        VàoRaThiếtBịCuối.ghi("vncd / HiểnThịTừXa start|stop|status: VNC :5900 (장치별 giáTrịMậtKhẩu)\n");
        VàoRaThiếtBịCuối.ghi("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        VàoRaThiếtBịCuối.ghi("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        VàoRaThiếtBịCuối.ghi("wc grep head tail tee env export unset history sh source true false exit\n");
        VàoRaThiếtBịCuối.ghi("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        VàoRaThiếtBịCuối.ghi("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        VàoRaThiếtBịCuối.ghi("giáTrịGóc + bênTrái 버튼 giáTrịKéo: thiếtBịCuối cỡ đổiGiáTrị; terminal size: giáTrịCột/giáTrịHàng\n");
        VàoRaThiếtBịCuối.ghi("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        VàoRaThiếtBịCuối.ghi("vi FILE: i to insert; Esc then :wq to save and quit\n");
        VàoRaThiếtBịCuối.ghi("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        VàoRaThiếtBịCuối.ghi("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        VàoRaThiếtBịCuối.ghi("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        VàoRaThiếtBịCuối.ghi("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        VàoRaThiếtBịCuối.ghi("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        VàoRaThiếtBịCuối.ghi("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        VàoRaThiếtBịCuối.ghi("python FILE.py | python -c 'CODE' (MicroPython)\n");
        VàoRaThiếtBịCuối.ghi("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        VàoRaThiếtBịCuối.ghi("pip: MicroPython câyNguồn càiĐặtGiáTrị; Chủ --network --pip giáTrịCầnĐến; /lib는 RAM\n");
        VàoRaThiếtBịCuối.ghi("gui | run cpp | net test | tasks | selftest | samples\n");
        VàoRaThiếtBịCuối.ghi("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        VàoRaThiếtBịCuối.ghi("/example/java /example/c /example/python: examples ready at boot\n");
        VàoRaThiếtBịCuối.ghi("example java|c|python: restore missing examples (keeps existing files)\n");
        trợGiúpHangul();
    }
    static void thiếtBịCuối(boolean đãChuyểnĐãLà) {
        if (đãChuyểnĐãLà && BoMạch.thiếtBịCuối(2) != 0) { BoMạch.thiếtBịCuối(0); VàoRaThiếtBịCuối.ghi("TERMINAL CLOSED\n"); }
        else if (BoMạch.thiếtBịCuối(1) < 0) lỗi(-19);
        else VàoRaThiếtBịCuối.ghi("TERMINAL READY — Tiếng Việt terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void lệnh() {
        if (sốLượngTừTố == 0) return;
        if (côngCụHệThống.thựcThiLệnh()) return;
        if (vănBảnBằng(0,"sshd") || vănBảnBằng(0,"vỏLệnhAnToàn") || vănBảnBằng(0,"vncd") || vănBảnBằng(0,"HiểnThịTừXa")) {
            int giáTrịLoại=vănBảnBằng(0,"vncd")||vănBảnBằng(0,"HiểnThịTừXa")?1:0;
            int hànhĐộng=vănBảnBằng(1,"start")||vănBảnBằng(1,"chạy")?1:vănBảnBằng(1,"stop")||vănBảnBằng(1,"dừng")?0:2;
            int giáTrịTrạngThái=BoMạch.điềuKhiểnTừXa(giáTrịLoại,hànhĐộng);
            if(giáTrịTrạngThái<0)lỗi(giáTrịTrạngThái);else VàoRaThiếtBịCuối.ghi(BoMạch.điềuKhiểnTừXa(giáTrịLoại,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (vănBảnBằng(0, "help") || vănBảnBằng(0, "h")) { if (vănBảnBằng(1, "ko") || vănBảnBằng(1, "input")) trợGiúpHangul(); else hiệnTrợGiúp(); }
        else if (vănBảnBằng(0, "info") || vănBảnBằng(0, "i")) Nhân.thôngTinHệThống();
        else if (vănBảnBằng(0, "pwd")) { CácTệpBộNhớ.ghiHiệnTại(); VàoRaThiếtBịCuối.KýTự(10); }
        else if (vănBảnBằng(0, "cd")) {
            int giáTrịĐãXửLý;
            if (sốLượngTừTố == 1) { CácTệpBộNhớ.bắtChạyĐườngDẫn(1); giáTrịĐãXửLý = CácTệpBộNhớ.byteĐườngDẫn(0, '/'); } else giáTrịĐãXửLý = sốLượngTừTố == 2 ? đườngDẫn(1) : -22;
            if (giáTrịĐãXửLý >= 0) giáTrịĐãXửLý = CácTệpBộNhớ.đổiThưMục(); if (giáTrịĐãXửLý < 0) lỗi(giáTrịĐãXửLý);
        }
        else if (vănBảnBằng(0, "ls") || vănBảnBằng(0, "f")) {
            int chỉSốĐốiSố = vănBảnBằng(1, "-l") ? 2 : 1, giáTrịĐãXửLý;
            if (sốLượngTừTố == chỉSốĐốiSố) { CácTệpBộNhớ.bắtChạyĐườngDẫn(1); giáTrịĐãXửLý = CácTệpBộNhớ.byteĐườngDẫn(0, '.'); } else giáTrịĐãXửLý = sốLượngTừTố == chỉSốĐốiSố + 1 ? đườngDẫn(chỉSốĐốiSố) : -22;
            if (giáTrịĐãXửLý >= 0) giáTrịĐãXửLý = CácTệpBộNhớ.cácMụcĐườngDẫn(); if (giáTrịĐãXửLý < 0) lỗi(giáTrịĐãXửLý);
        }
        else if (vănBảnBằng(0, "mkdir") || vănBảnBằng(0, "rmdir") || vănBảnBằng(0, "touch")) CácCôngCụVỏLệnh.côngViệcTệp(vănBảnBằng(0, "mkdir") ? "mkdir" : vănBảnBằng(0, "rmdir") ? "rmdir" : "touch");
        else if (vănBảnBằng(0, "cp") || vănBảnBằng(0, "mv")) CácCôngCụVỏLệnh.saoChépGiáTrị(vănBảnBằng(0, "mv"));
        else if (vănBảnBằng(0, "cat")) CácCôngCụVỏLệnh.giáTrịKhungNhìn();
        else if (vănBảnBằng(0, "wc")) CácCôngCụVỏLệnh.giáTrịViệcĐếm();
        else if (vănBảnBằng(0, "grep")) CácCôngCụVỏLệnh.tìmMục();
        else if (vănBảnBằng(0, "head") || vănBảnBằng(0, "tail")) CácCôngCụVỏLệnh.giáTrịĐầu(vănBảnBằng(0, "tail"));
        else if (vănBảnBằng(0, "tee")) CácCôngCụVỏLệnh.ghiCùng();
        else if (vănBảnBằng(0, "env")) CúPhápVỏLệnh.hiệnMôiTrường();
        else if (vănBảnBằng(0, "export") || vănBảnBằng(0, "unset")) {
            if (sốLượngTừTố == 1) CúPhápVỏLệnh.hiệnMôiTrường();
            for (int chỉSốVòngLặp = 1; chỉSốVòngLặp < sốLượngTừTố; chỉSốVòngLặp++) { int giáTrịĐãXửLý = CúPhápVỏLệnh.cácThiếtLậpMôiTrường(chỉSốVòngLặp, vănBảnBằng(0, "unset")); if (giáTrịĐãXửLý != 0) { kếtQuả = giáTrịĐãXửLý; VàoRaThiếtBịCuối.ghi("lệnh phânTíchCúPhápGiáTrị: giáTrịBiến 이름이 잘못되었거나 예약된 이름이거나 môiTrường 공간이 가득 찼습니다\n"); } }
        }
        else if (vănBảnBằng(0, "sh") || vănBảnBằng(0, "source")) CúPhápVỏLệnh.thựcThiTệp();
        else if (vănBảnBằng(0, "true")) kếtQuả = 0;
        else if (vănBảnBằng(0, "false")) kếtQuả = 1;
        else if (vănBảnBằng(0, "history")) TrìnhSoạnThảoDòng.hiệnNhậtKý();
        else if (vănBảnBằng(0, "exit")) {
            if (CúPhápVỏLệnh.giáTrịĐộSâu > 0) { kếtQuả = sốLượngTừTố == 1 ? CúPhápVỏLệnh.giáTrịTrạngThái : CácCôngCụVỏLệnh.giáTrịChữSố(1); if (kếtQuả < 0 || kếtQuả > 255) kếtQuả = 2; CúPhápVỏLệnh.kếtThúcKịchBản = true; }
            else if (BoMạch.thiếtBịCuối(2) != 0) thiếtBịCuối(true);
            else VàoRaThiếtBịCuối.ghi("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (vănBảnBằng(0, "edit")) giáTrịSửa();
        else if (vănBảnBằng(0, "load") || vănBảnBằng(0, "hex")) vàoRaNhịPhân(vănBảnBằng(0, "load"));
        else if (vănBảnBằng(0, "rm")) {
            if (sốLượngTừTố < 2) { kếtQuả = 2; VàoRaThiếtBịCuối.ghi("사용법: rm Tệp...\n"); }
            for (int chỉSốVòngLặp = 1; chỉSốVòngLặp < sốLượngTừTố; chỉSốVòngLặp++) { int giáTrịĐãXửLý = đườngDẫn(chỉSốVòngLặp); if (giáTrịĐãXửLý == 0) giáTrịĐãXửLý = CácTệpBộNhớ.xóaMục(); if (giáTrịĐãXửLý < 0) lỗi(giáTrịĐãXửLý); }
        }
        else if (vănBảnBằng(0, "echo")) {
            int bắtChạyVịTrí = vănBảnBằng(1, "-n") ? 2 : 1;
            for (int dữLiệuĐầuTiên = bắtChạyVịTrí; dữLiệuĐầuTiên < sốLượngTừTố; dữLiệuĐầuTiên++) { if (dữLiệuĐầuTiên > bắtChạyVịTrí) VàoRaThiếtBịCuối.KýTự(32); for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < độDài[dữLiệuĐầuTiên]; chỉSốVòngLặp++) BoMạch.ghiNốiTiếp(giáTrịTừTố[điểmĐangBắtChạy[dữLiệuĐầuTiên] + chỉSốVòngLặp]); }
            if (bắtChạyVịTrí == 1) VàoRaThiếtBịCuối.KýTự(10);
        }
        else if (vănBảnBằng(0, "clear")) VàoRaThiếtBịCuối.ghi("\u001b[2J\u001b[H");
        else if (vănBảnBằng(0, "javac") || vănBảnBằng(0, "java") || vănBảnBằng(0, "python") || vănBảnBằng(0, "pip")) {
            int giáTrịĐãXửLý = vănBảnBằng(0, "pip") ? GóiGộpPython() : CôngCụ(vănBảnBằng(0, "javac") ? 10 : vănBảnBằng(0, "java") ? 11 : 12); kếtQuả = giáTrịĐãXửLý == -1005 ? -1005 : giáTrịĐãXửLý < 0 ? 126 : giáTrịĐãXửLý;
            if (giáTrịĐãXửLý != -1005 && !CúPhápVỏLệnh.làĐangKếtNối) { VàoRaThiếtBịCuối.ghi("exit "); VàoRaThiếtBịCuối.trịSố(giáTrịĐãXửLý); VàoRaThiếtBịCuối.KýTự(10); }
        }
        else if (vănBảnBằng(0, "vi")) { int giáTrịĐãXửLý = CôngCụ(13); kếtQuả = giáTrịĐãXửLý == -1005 ? -1005 : giáTrịĐãXửLý < 0 ? 126 : giáTrịĐãXửLý; }
        else if (vănBảnBằng(0, "cc") || vănBảnBằng(0, "tcc")) { int giáTrịĐãXửLý = CôngCụ(15); kếtQuả = giáTrịĐãXửLý < 0 ? 126 : giáTrịĐãXửLý; if (!CúPhápVỏLệnh.làĐangKếtNối) { VàoRaThiếtBịCuối.ghi("exit "); VàoRaThiếtBịCuối.trịSố(giáTrịĐãXửLý); VàoRaThiếtBịCuối.KýTự(10); } }
        else if (vănBảnBằng(0, "jaot")) { int giáTrịĐãXửLý = CôngCụ(16); kếtQuả = giáTrịĐãXửLý < 0 ? 126 : giáTrịĐãXửLý; if (!CúPhápVỏLệnh.làĐangKếtNối) { VàoRaThiếtBịCuối.ghi("exit "); VàoRaThiếtBịCuối.trịSố(giáTrịĐãXửLý); VàoRaThiếtBịCuối.KýTự(10); } }
        else if (vănBảnBằng(0, "terminal")) {
            if (vănBảnBằng(1, "size")) { int cỡ = BoMạch.thiếtBịCuối(13); VàoRaThiếtBịCuối.ghi("TERMINAL SIZE "); VàoRaThiếtBịCuối.trịSố(cỡ & 65535); VàoRaThiếtBịCuối.KýTự('x'); VàoRaThiếtBịCuối.trịSố(cỡ >>> 16); VàoRaThiếtBịCuối.KýTự(10); }
            else thiếtBịCuối(false);
        }
        else if (vănBảnBằng(0, "gui") || vănBảnBằng(0, "v")) { BoMạch.thiếtBịCuối(9); MànLàmViệc.thựcThiLệnh(); }
        else if (vănBảnBằng(0, "c")) Nhân.thửC();
        else if (vănBảnBằng(0, "tasks") || vănBảnBằng(0, "t")) Nhân.thửCácTácVụ();
        else if (vănBảnBằng(0, "g")) Nhân.MànHình();
        else if (vănBảnBằng(0, "selftest") || vănBảnBằng(0, "u")) Nhân.thửCácChươngTrìnhNgườiDùng();
        else if (vănBảnBằng(0, "e") || (vănBảnBằng(0, "run") && vănBảnBằng(1, "cpp"))) {
            int giáTrịĐãXửLý = BoMạch.chạyChươngTrìnhNgườiDùng(0); if (giáTrịĐãXửLý == 0) VàoRaThiếtBịCuối.ghi("ELF DEMO PASS\n"); else lỗi(giáTrịĐãXửLý);
        }
        else if (vănBảnBằng(0, "run")) { int giáTrịĐãXửLý = vănBảnBằng(1, "--linux") ? MụcCôngCụ(-2, 2) : CôngCụ(-1); kếtQuả = giáTrịĐãXửLý == -1005 ? -1005 : giáTrịĐãXửLý < 0 ? 126 : giáTrịĐãXửLý; if (giáTrịĐãXửLý != -1005 && !CúPhápVỏLệnh.làĐangKếtNối) { VàoRaThiếtBịCuối.ghi("exit "); VàoRaThiếtBịCuối.trịSố(giáTrịĐãXửLý); VàoRaThiếtBịCuối.KýTự(10); } }
        else if (vănBảnBằng(0, "n") || (vănBảnBằng(0, "net") && vănBảnBằng(1, "test"))) Nhân.thửKếtNốiMạng();
        else if (vănBảnBằng(0, "ftpd")) {
            if (vănBảnBằng(1, "start")) { int giáTrịĐãXửLý = BoMạch.dịchVụChuyểnGiaoTệp(1); if (giáTrịĐãXửLý < 0) lỗi(giáTrịĐãXửLý); else { VàoRaThiếtBịCuối.ghi("FTP listening "); côngCụHệThống.ghiĐịaChỉ(BoMạch.tìnhTrạngMạng(0,0)); VàoRaThiếtBịCuối.ghi(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (vănBảnBằng(1, "stop")) { BoMạch.dịchVụChuyểnGiaoTệp(0); VàoRaThiếtBịCuối.ghi("FTP stopped\n"); }
            else VàoRaThiếtBịCuối.ghi(BoMạch.dịchVụChuyểnGiaoTệp(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (vănBảnBằng(0, "samples")) { GóiGộp.chuẩnBị(); VàoRaThiếtBịCuối.ghi("SAMPLES READY (existing files kept)\n"); }
        else if (vănBảnBằng(0, "example")) {
            int NgônNgữ = vănBảnBằng(1, "java") ? 0 : vănBảnBằng(1, "c") ? 1 : vănBảnBằng(1, "python") ? 2 : -1;
            if (sốLượngTừTố != 2 || NgônNgữ < 0) VàoRaThiếtBịCuối.ghi("example java|c|python: ĐầuRa, Tệp, 네트워크, 그래픽, Java Swing cửaSổ VíDụ\n");
            else { int giáTrịĐãXửLý = GóiGộpVíDụ.càiĐặtGiáTrị(NgônNgữ); if (giáTrịĐãXửLý < 0) { lỗi(giáTrịĐãXửLý); if (giáTrịĐãXửLý == -28) VàoRaThiếtBịCuối.ghi("RAM full: remove unused files, then retry example\n"); } else VàoRaThiếtBịCuối.ghi("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int giáTrịĐịnhDạng = địnhDạngViệcThựcThi();
            if (giáTrịĐịnhDạng == 1 || giáTrịĐịnhDạng == 2) {
                int giáTrịĐãXửLý = MụcCôngCụ(giáTrịĐịnhDạng == 1 ? -1 : 14, 0); kếtQuả = giáTrịĐãXửLý == -1005 ? -1005 : giáTrịĐãXửLý < 0 ? 126 : giáTrịĐãXửLý;
                if (giáTrịĐãXửLý != -1005 && !CúPhápVỏLệnh.làĐangKếtNối) { VàoRaThiếtBịCuối.ghi("exit "); VàoRaThiếtBịCuối.trịSố(giáTrịĐãXửLý); VàoRaThiếtBịCuối.KýTự(10); }
            } else if (giáTrịĐịnhDạng == 0) { kếtQuả = 126; VàoRaThiếtBịCuối.ghi("실행할 trịSố 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { kếtQuả = 127; VàoRaThiếtBịCuối.ghi("Unknown command. help: commands\n"); }
        }
    }
    public static void thựcThiLệnh() {
        GóiGộp.chuẩnBị();
        for (int NgônNgữ = 0; NgônNgữ < 3; NgônNgữ++) { int giáTrịĐãXửLý = GóiGộpVíDụ.càiĐặtGiáTrị(NgônNgữ); if (giáTrịĐãXửLý < 0) lỗi(giáTrịĐãXửLý); }
        hiệnTrợGiúp();
        while (true) {
            phiênCửaSổ.mụcGiáTrịTiếnTrình(); if (phiênCửaSổ.việcThựcThiTiếpDiễn()) continue;
            if (!phiênCửaSổ.đọcSựTiếpDiễn) VàoRaThiếtBịCuối.ghi("jkoros-native> "); TrìnhSoạnThảoDòng.dòngLệnh = true; BoMạch.chờTừXa(1); int cỡ = đọcDòngĐầuVào(); BoMạch.chờTừXa(0); TrìnhSoạnThảoDòng.dòngLệnh = false;
            if (cỡ == -3) continue;
            if (cỡ == -2) VàoRaThiếtBịCuối.ghi("lệnh phânTíchCúPhápGiáTrị: 명령줄이 너무 깁니다\n");
            if (cỡ >= 0) { CúPhápVỏLệnh.kếtThúcKịchBản = false; CúPhápVỏLệnh.thựcThiLệnh(dòng, 0, cỡ, 0); } else CúPhápVỏLệnh.giáTrịTrạngThái = 130;
            BoMạch.lệnhTừXaKếtThúc(CúPhápVỏLệnh.giáTrịTrạngThái);
            TrìnhSoạnThảoDòng.cỡ = TrìnhSoạnThảoDòng.giáTrịConTrỏVănBản = TrìnhSoạnThảoDòng.bắtChạyCửaSổ = 0;
        }
    }
}
