// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 64 tệp RAM, mỗi tệp 16384 byte, 16 bộ mô tả. Toàn bộ dữ liệu và chính sách nằm trong Java. Lời gọi không nhường quyền chạy nên là nguyên tử giữa các tác vụ hợp tác trên một lõi hiện tại. Đây không phải lưu trữ đĩa hay bản triển khai POSIX đầy đủ. Giá trị âm là mã lỗi. */
public final class CácTệpBộNhớ {
    static final int sốLượngTệp = 64;
    static int[] tên = new int[sốLượngTệp * 64];
    static int[] độDàiTên = new int[sốLượngTệp];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] giáTrịNộiDung = new int[sốLượngTệp * 4096];
    static int[] độDài = new int[sốLượngTệp];
    static int[] sốLượngThamChiếu = new int[sốLượngTệp];
    static int[] giáTrịDùng = new int[16];
    static int[] giáTrịĐốiĐích = new int[16];
    static int[] vịTrí = new int[16];
    static int[] chếĐộPhươngThức = new int[16];
    static int[] đườngDẫn = new int[64];
    static int độDàiĐườngDẫn;

    public static int giớiHạnTệp() { return sốLượngTệp; }
    static int đọcDữLiệu(int Tệp, int chỉSốVịTrí) { return (giáTrịNộiDung[Tệp * 4096 + chỉSốVịTrí / 4] >>> ((chỉSốVịTrí & 3) * 8)) & 255; }
    static void ghiDữLiệu(int Tệp, int chỉSốVịTrí, int giáTrị) {
        int mụcÔ = Tệp * 4096 + chỉSốVịTrí / 4, giáTrịDiChuyển = (chỉSốVịTrí & 3) * 8;
        giáTrịNộiDung[mụcÔ] = (giáTrịNộiDung[mụcÔ] & ~(255 << giáTrịDiChuyển)) | ((giáTrị & 255) << giáTrịDiChuyển);
    }

    public static int bắtChạyĐườngDẫn(int cỡ) {
        độDàiĐườngDẫn = 0;
        if (cỡ < 1 || cỡ > 63) return -36;
        độDàiĐườngDẫn = cỡ;
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < cỡ; chỉSốVòngLặp++) đườngDẫn[chỉSốVòngLặp] = 0;
        return 0;
    }
    public static int byteĐườngDẫn(int sốHiệu, int giáTrị) {
        if (sốHiệu < 0 || sốHiệu >= độDàiĐườngDẫn || giáTrị < 1 || giáTrị > 255) return -22;
        đườngDẫn[sốHiệu] = giáTrị; return 0;
    }
    static int tìmMục() {
        for (int chỉSốTệp = 0; chỉSốTệp < sốLượngTệp; chỉSốTệp++) if (độDàiTên[chỉSốTệp] > 0 && độDàiTên[chỉSốTệp] == độDàiChuẩnTắc && giáTrịTiềnTố(tên, chỉSốTệp * 64, độDàiTên[chỉSốTệp], giáTrịChuẩnTắc, độDàiChuẩnTắc)) return chỉSốTệp;
        return -1;
    }
    public static int mở(int giáTrịCácCờ) {
        if (độDàiĐườngDẫn == 0 || (giáTrịCácCờ & ~0x6c3) != 0 || (giáTrịCácCờ & 3) == 3) return -22;
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < độDàiĐườngDẫn; chỉSốVòngLặp++) if (đườngDẫn[chỉSốVòngLặp] == 0) return -22;
        if ((giáTrịCácCờ & 0x200) != 0 && (giáTrịCácCờ & 3) == 0) return -22;
        int kếtQuả = chuẩnHóaGiáTrị(); if (kếtQuả < 0) return kếtQuả;
        if (tìmThưMục(độDàiChuẩnTắc) >= 0) return -21;
        kếtQuả = kiểmTraCha(); if (kếtQuả < 0) return kếtQuả;
        int Tệp = tìmMục();
        if (Tệp >= 0 && (giáTrịCácCờ & 0xc0) == 0xc0) return -17;
        if (Tệp < 0 && (giáTrịCácCờ & 0x40) == 0) return -2;
        int mụcBộMôTả = -1;
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < 16; chỉSốVòngLặp++) if (giáTrịDùng[chỉSốVòngLặp] == 0) { mụcBộMôTả = chỉSốVòngLặp; break; }
        if (mụcBộMôTả < 0) return -24;
        if (Tệp < 0) {
            for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < sốLượngTệp; chỉSốVòngLặp++) if (độDàiTên[chỉSốVòngLặp] == 0 && sốLượngThamChiếu[chỉSốVòngLặp] == 0) { Tệp = chỉSốVòngLặp; break; }
            if (Tệp < 0) return -28;
            độDàiTên[Tệp] = độDàiChuẩnTắc;
            for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < độDàiChuẩnTắc; chỉSốVòngLặp++) tên[Tệp * 64 + chỉSốVòngLặp] = giáTrịChuẩnTắc[chỉSốVòngLặp];
            độDài[Tệp] = 0;
        }
        if ((giáTrịCácCờ & 0x200) != 0) độDài[Tệp] = 0;
        giáTrịDùng[mụcBộMôTả] = 1; giáTrịĐốiĐích[mụcBộMôTả] = Tệp; vịTrí[mụcBộMôTả] = 0; chếĐộPhươngThức[mụcBộMôTả] = giáTrịCácCờ;
        sốLượngThamChiếu[Tệp]++;
        return mụcBộMôTả + 3;
    }
    static int xácMinh(int mụcBộMôTả) {
        return mụcBộMôTả >= 3 && mụcBộMôTả < 19 && giáTrịDùng[mụcBộMôTả - 3] != 0 ? mụcBộMôTả - 3 : -1;
    }
    public static int đọc(int mụcBộMôTả) {
        int mụcÔ = xácMinh(mụcBộMôTả);
        if (mụcÔ < 0 || (chếĐộPhươngThức[mụcÔ] & 3) == 1) return -9;
        int Tệp = giáTrịĐốiĐích[mụcÔ];
        if (vịTrí[mụcÔ] >= độDài[Tệp]) return 256; // Phân biệt EOF với các byte thực 0x00..0xff.
        return đọcDữLiệu(Tệp, vịTrí[mụcÔ]++);
    }
    public static int ghi(int mụcBộMôTả, int giáTrị) {
        int mụcÔ = xácMinh(mụcBộMôTả);
        if (mụcÔ < 0 || (chếĐộPhươngThức[mụcÔ] & 3) == 0) return -9;
        int Tệp = giáTrịĐốiĐích[mụcÔ];
        if ((chếĐộPhươngThức[mụcÔ] & 0x400) != 0) vịTrí[mụcÔ] = độDài[Tệp];
        if (vịTrí[mụcÔ] >= 16384) return -28;
        while (độDài[Tệp] < vịTrí[mụcÔ]) ghiDữLiệu(Tệp, độDài[Tệp]++, 0);
        ghiDữLiệu(Tệp, vịTrí[mụcÔ]++, giáTrị);
        if (độDài[Tệp] < vịTrí[mụcÔ]) độDài[Tệp] = vịTrí[mụcÔ];
        return 1;
    }
    public static int dịchVịVịTrí(int mụcBộMôTả, int giáTrịKhoảngCách, int gốcCâyDựÁn) {
        int mụcÔ = xácMinh(mụcBộMôTả);
        if (mụcÔ < 0) return -9;
        if (gốcCâyDựÁn < 0 || gốcCâyDựÁn > 2 || giáTrịKhoảngCách < -16384 || giáTrịKhoảngCách > 16384) return -22;
        int vịTríMới = giáTrịKhoảngCách + (gốcCâyDựÁn == 0 ? 0 : gốcCâyDựÁn == 1 ? vịTrí[mụcÔ] : độDài[giáTrịĐốiĐích[mụcÔ]]);
        if (vịTríMới < 0 || vịTríMới > 16384) return -22;
        vịTrí[mụcÔ] = vịTríMới; return vịTríMới;
    }
    public static int đóng(int mụcBộMôTả) {
        int mụcÔ = xácMinh(mụcBộMôTả);
        if (mụcÔ < 0) return -9;
        sốLượngThamChiếu[giáTrịĐốiĐích[mụcÔ]]--; giáTrịDùng[mụcÔ] = 0; return 0;
    }
    public static int cỡ(int mụcBộMôTả) {
        int mụcÔ = xácMinh(mụcBộMôTả); return mụcÔ < 0 ? -9 : độDài[giáTrịĐốiĐích[mụcÔ]];
    }
    public static int đặtGiáTrịĐộDài(int mụcBộMôTả, int cỡ) {
        int mụcÔ = xácMinh(mụcBộMôTả);
        if (mụcÔ < 0 || (chếĐộPhươngThức[mụcÔ] & 3) == 0) return -9;
        if (cỡ < 0 || cỡ > 16384) return -22;
        int Tệp = giáTrịĐốiĐích[mụcÔ];
        while (độDài[Tệp] < cỡ) ghiDữLiệu(Tệp, độDài[Tệp]++, 0);
        độDài[Tệp] = cỡ; return 0;
    }
    public static int xóaMục() {
        if (độDàiĐườngDẫn == 0) return -22;
        int kếtQuả = chuẩnHóaGiáTrị(); if (kếtQuả < 0) return kếtQuả;
        if (tìmThưMục(độDàiChuẩnTắc) >= 0) return -21;
        kếtQuả = kiểmTraCha(); if (kếtQuả < 0) return kếtQuả;
        int Tệp = tìmMục();
        if (Tệp < 0) return -2;
        độDàiTên[Tệp] = 0; return 0; // Giữ tệp đang mở cho tới lần close cuối cùng.
    }
    static void danhSáchMục() {
        bắtChạyĐườngDẫn(1); byteĐườngDẫn(0, '.'); cácMụcĐườngDẫn();
    }
    public static int độDàiTênĐãXuất(int sốHiệu) {
        if (sốHiệu < 0 || sốHiệu >= sốLượngTệp || độDàiTên[sốHiệu] == 0) return 0;
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < độDàiTên[sốHiệu]; chỉSốVòngLặp++) if (tên[sốHiệu * 64 + chỉSốVòngLặp] == '/') return 0;
        return độDàiTên[sốHiệu];
    }
    public static int byteTênĐãXuất(int sốHiệu, int chỉSốVịTrí) {
        return sốHiệu >= 0 && sốHiệu < sốLượngTệp && chỉSốVịTrí >= 0 && chỉSốVịTrí < độDàiTên[sốHiệu] ? tên[sốHiệu * 64 + chỉSốVịTrí] : -22;
    }
    public static int cỡTệpĐãXuất(int sốHiệu) { return sốHiệu >= 0 && sốHiệu < sốLượngTệp ? độDài[sốHiệu] : -22; }
    static int[] giáTrịChuẩnTắc = new int[64], phầnMụcHiệnTại = new int[64], tênThưMục = new int[16 * 64], độDàiThưMục = new int[16];
    static int độDàiChuẩnTắc, độDàiHiệnTại;
    static boolean giáTrịTiềnTố(int[] danhSáchCácTên, int chạy, int giáTrịĐườngDẫn, int[] giáTrịPhíaTrước, int đườngDẫnDẫnĐầu) {
        if (giáTrịĐườngDẫn < đườngDẫnDẫnĐầu) return false;
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < đườngDẫnDẫnĐầu; chỉSốVòngLặp++) if (danhSáchCácTên[chạy + chỉSốVòngLặp] != giáTrịPhíaTrước[chỉSốVòngLặp]) return false;
        return true;
    }
    static int chuẩnHóaGiáTrị() {
        if (độDàiĐườngDẫn == 0) return -22;
        độDàiChuẩnTắc = đườngDẫn[0] == '/' ? 0 : độDàiHiệnTại;
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < độDàiChuẩnTắc; chỉSốVòngLặp++) giáTrịChuẩnTắc[chỉSốVòngLặp] = phầnMụcHiệnTại[chỉSốVòngLặp];
        int đọcConTrỏVănBản = 0;
        while (đọcConTrỏVănBản < độDàiĐườngDẫn) {
            while (đọcConTrỏVănBản < độDàiĐườngDẫn && đườngDẫn[đọcConTrỏVănBản] == '/') đọcConTrỏVănBản++;
            int bắtChạyVịTrí = đọcConTrỏVănBản; while (đọcConTrỏVănBản < độDàiĐườngDẫn && đườngDẫn[đọcConTrỏVănBản] != '/') { if (đườngDẫn[đọcConTrỏVănBản] == 0) return -22; đọcConTrỏVănBản++; }
            int sốLượngMục = đọcConTrỏVănBản - bắtChạyVịTrí; if (sốLượngMục == 0 || sốLượngMục == 1 && đườngDẫn[bắtChạyVịTrí] == '.') continue;
            if (sốLượngMục == 2 && đườngDẫn[bắtChạyVịTrí] == '.' && đườngDẫn[bắtChạyVịTrí + 1] == '.') {
                while (độDàiChuẩnTắc > 0 && giáTrịChuẩnTắc[độDàiChuẩnTắc - 1] != '/') độDàiChuẩnTắc--;
                if (độDàiChuẩnTắc > 0) độDàiChuẩnTắc--;
                continue;
            }
            if (độDàiChuẩnTắc + sốLượngMục + (độDàiChuẩnTắc == 0 ? 0 : 1) > 63) return -36;
            if (độDàiChuẩnTắc > 0) giáTrịChuẩnTắc[độDàiChuẩnTắc++] = '/';
            for (int chỉSốVòngLặp = bắtChạyVịTrí; chỉSốVòngLặp < đọcConTrỏVănBản; chỉSốVòngLặp++) giáTrịChuẩnTắc[độDàiChuẩnTắc++] = đườngDẫn[chỉSốVòngLặp];
        }
        return 0;
    }
    static int tìmThưMục(int sốLượngMục) {
        if (sốLượngMục == 0) return 0;
        for (int chỉSốVòngLặp = 1; chỉSốVòngLặp < 16; chỉSốVòngLặp++) if (độDàiThưMục[chỉSốVòngLặp] == sốLượngMục && giáTrịTiềnTố(tênThưMục, chỉSốVòngLặp * 64, sốLượngMục, giáTrịChuẩnTắc, sốLượngMục)) return chỉSốVòngLặp;
        return -1;
    }
    static int kiểmTraCha() {
        int sốLượngMục = độDàiChuẩnTắc; while (sốLượngMục > 0 && giáTrịChuẩnTắc[sốLượngMục - 1] != '/') sốLượngMục--;
        return tìmThưMục(sốLượngMục == 0 ? 0 : sốLượngMục - 1) < 0 ? -2 : 0;
    }
    public static int tạoThưMục() {
        int giáTrịĐãXửLý = chuẩnHóaGiáTrị(); if (giáTrịĐãXửLý < 0) return giáTrịĐãXửLý;
        if (tìmThưMục(độDàiChuẩnTắc) >= 0 || tìmMục() >= 0) return -17;
        giáTrịĐãXửLý = kiểmTraCha(); if (giáTrịĐãXửLý < 0) return giáTrịĐãXửLý;
        for (int chỉSốVòngLặp = 1; chỉSốVòngLặp < 16; chỉSốVòngLặp++) if (độDàiThưMục[chỉSốVòngLặp] == 0) {
            độDàiThưMục[chỉSốVòngLặp] = độDàiChuẩnTắc; for (int vịTríPhíaTrong = 0; vịTríPhíaTrong < độDàiChuẩnTắc; vịTríPhíaTrong++) tênThưMục[chỉSốVòngLặp * 64 + vịTríPhíaTrong] = giáTrịChuẩnTắc[vịTríPhíaTrong]; return 0;
        }
        return -28;
    }
    public static int loạiMục() {
        int giáTrịĐãXửLý = chuẩnHóaGiáTrị(); if (giáTrịĐãXửLý < 0) return giáTrịĐãXửLý;
        if (tìmThưMục(độDàiChuẩnTắc) >= 0) return 2;
        return tìmMục() >= 0 ? 1 : 0;
    }
    public static int đổiThưMục() {
        int giáTrịĐãXửLý = chuẩnHóaGiáTrị(); if (giáTrịĐãXửLý < 0) return giáTrịĐãXửLý;
        if (tìmThưMục(độDàiChuẩnTắc) < 0) return -2;
        độDàiHiệnTại = độDàiChuẩnTắc; for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < độDàiHiệnTại; chỉSốVòngLặp++) phầnMụcHiệnTại[chỉSốVòngLặp] = giáTrịChuẩnTắc[chỉSốVòngLặp]; return 0;
    }
    public static int gỡThưMục() {
        int giáTrịĐãXửLý = chuẩnHóaGiáTrị(); if (giáTrịĐãXửLý < 0) return giáTrịĐãXửLý;
        int sốThưMục = tìmThưMục(độDàiChuẩnTắc); if (sốThưMục < 0) return -2; if (sốThưMục == 0) return -16;
        if (độDàiHiệnTại == độDàiChuẩnTắc && giáTrịTiềnTố(phầnMụcHiệnTại, 0, độDàiHiệnTại, giáTrịChuẩnTắc, độDàiChuẩnTắc)) return -16;
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < sốLượngTệp; chỉSốVòngLặp++) {
            if (độDàiTên[chỉSốVòngLặp] > độDàiChuẩnTắc && giáTrịTiềnTố(tên, chỉSốVòngLặp * 64, độDàiTên[chỉSốVòngLặp], giáTrịChuẩnTắc, độDàiChuẩnTắc) && tên[chỉSốVòngLặp * 64 + độDàiChuẩnTắc] == '/') return -39;
        }
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < 16; chỉSốVòngLặp++) {
            if (độDàiThưMục[chỉSốVòngLặp] > độDàiChuẩnTắc && giáTrịTiềnTố(tênThưMục, chỉSốVòngLặp * 64, độDàiThưMục[chỉSốVòngLặp], giáTrịChuẩnTắc, độDàiChuẩnTắc) && tênThưMục[chỉSốVòngLặp * 64 + độDàiChuẩnTắc] == '/') return -39;
        }
        độDàiThưMục[sốThưMục] = 0; return 0;
    }
    public static int đổiTênMục(int sốNguyênBản) {
        if (sốNguyênBản < 0 || sốNguyênBản >= sốLượngTệp || độDàiTên[sốNguyênBản] == 0) return -2;
        int giáTrịĐãXửLý = chuẩnHóaGiáTrị(); if (giáTrịĐãXửLý < 0) return giáTrịĐãXửLý;
        if (tìmThưMục(độDàiChuẩnTắc) >= 0) return -21;
        giáTrịĐãXửLý = kiểmTraCha(); if (giáTrịĐãXửLý < 0) return giáTrịĐãXửLý;
        int giáTrịTrướcĐó = tìmMục(); if (giáTrịTrướcĐó == sốNguyênBản) return 0;
        if (giáTrịTrướcĐó >= 0) độDàiTên[giáTrịTrướcĐó] = 0;
        độDàiTên[sốNguyênBản] = độDàiChuẩnTắc; for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < độDàiChuẩnTắc; chỉSốVòngLặp++) tên[sốNguyênBản * 64 + chỉSốVòngLặp] = giáTrịChuẩnTắc[chỉSốVòngLặp]; return 0;
    }
    static int bắtChạyMục(int[] mảngDữLiệu, int điểmĐangBắtChạy, int sốLượngMục) {
        if (!giáTrịTiềnTố(mảngDữLiệu, điểmĐangBắtChạy, sốLượngMục, giáTrịChuẩnTắc, độDàiChuẩnTắc)) return -1;
        int bắtChạyVịTrí = độDàiChuẩnTắc;
        if (bắtChạyVịTrí > 0) { if (sốLượngMục <= bắtChạyVịTrí || mảngDữLiệu[điểmĐangBắtChạy + bắtChạyVịTrí] != '/') return -1; bắtChạyVịTrí++; }
        if (sốLượngMục <= bắtChạyVịTrí) return -1;
        for (int chỉSốVòngLặp = bắtChạyVịTrí; chỉSốVòngLặp < sốLượngMục; chỉSốVòngLặp++) if (mảngDữLiệu[điểmĐangBắtChạy + chỉSốVòngLặp] == '/') return -1;
        return bắtChạyVịTrí;
    }
    static void ghiHiệnTại() { VàoRaThiếtBịCuối.KýTự('/'); for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < độDàiHiệnTại; chỉSốVòngLặp++) BoMạch.ghiNốiTiếp(phầnMụcHiệnTại[chỉSốVòngLặp]); }
    static int cácMụcĐườngDẫn() {
        int giáTrịĐãXửLý = chuẩnHóaGiáTrị(); if (giáTrịĐãXửLý < 0) return giáTrịĐãXửLý;
        int giáTrịĐốiĐíchTệp = tìmMục();
        if (giáTrịĐốiĐíchTệp >= 0) { for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < độDàiChuẩnTắc; chỉSốVòngLặp++) BoMạch.ghiNốiTiếp(giáTrịChuẩnTắc[chỉSốVòngLặp]); VàoRaThiếtBịCuối.ghi("  "); VàoRaThiếtBịCuối.trịSố(độDài[giáTrịĐốiĐíchTệp]); VàoRaThiếtBịCuối.ghi("giáTrịByte(주기억 Tệp)\n"); return 0; }
        if (tìmThưMục(độDàiChuẩnTắc) < 0) return -2;
        for (int giáTrịỞCuối = 1; giáTrịỞCuối < 16; giáTrịỞCuối++) if (độDàiThưMục[giáTrịỞCuối] > 0) {
            int bắtChạyVịTrí = bắtChạyMục(tênThưMục, giáTrịỞCuối * 64, độDàiThưMục[giáTrịỞCuối]); if (bắtChạyVịTrí < 0) continue;
            for (int chỉSốVòngLặp = bắtChạyVịTrí; chỉSốVòngLặp < độDàiThưMục[giáTrịỞCuối]; chỉSốVòngLặp++) BoMạch.ghiNốiTiếp(tênThưMục[giáTrịỞCuối * 64 + chỉSốVòngLặp]); VàoRaThiếtBịCuối.ghi("/\n");
        }
        for (int chỉSốTệp = 0; chỉSốTệp < sốLượngTệp; chỉSốTệp++) if (độDàiTên[chỉSốTệp] > 0) {
            int bắtChạyVịTrí = bắtChạyMục(tên, chỉSốTệp * 64, độDàiTên[chỉSốTệp]); if (bắtChạyVịTrí < 0) continue;
            for (int chỉSốVòngLặp = bắtChạyVịTrí; chỉSốVòngLặp < độDàiTên[chỉSốTệp]; chỉSốVòngLặp++) BoMạch.ghiNốiTiếp(tên[chỉSốTệp * 64 + chỉSốVòngLặp]);
            VàoRaThiếtBịCuối.ghi("  "); VàoRaThiếtBịCuối.trịSố(độDài[chỉSốTệp]); VàoRaThiếtBịCuối.ghi("giáTrịByte(주기억 Tệp)\n");
        }
        return 0;
    }
}
