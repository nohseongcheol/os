// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Tách bộ mô tả tệp của một tiến trình người dùng khỏi mô tả tệp đang mở. Số lời gọi được ghi trong tài liệu POSIX ABI. */
public final class QuảnLýMôTảTệp {
    static final int giớiHạnBộMôTả = 32;
    static final int đọcCờGhi = 2, tạoMục = 64, tạoRiêng = 128, xóaSạchCácNộiDung = 512;
    static final int thêmCuốiSựTiếpDiễn = 1024, chờKhôngThựcHiện = 2048, đóngThựcThiẢnhBậtTrạngThái = 524288;
    static int[] mởThẻXửLý = new int[giớiHạnBộMôTả], đặtGiáTrịBộMôTả = new int[giớiHạnBộMôTả];
    static int[] giáTrịLoại = new int[giớiHạnBộMôTả], giáTrịĐốiĐích = new int[giớiHạnBộMôTả];
    static int[] vịTríTệp = new int[giớiHạnBộMôTả], mởCácThiếtLập = new int[giớiHạnBộMôTả], sốLượngThamChiếu = new int[giớiHạnBộMôTả];
    static int[] thẻXửLýMạng = new int[giớiHạnBộMôTả], nhậnMiliGiâyHếtGiờ = new int[giớiHạnBộMôTả];
    static int[] tênĐườngDẫn = new int[64], dữLiệuChuyểnGiao = new int[1024];

    static int tìmBộMôTả(int bộMôTảTệp) {
        if (bộMôTảTệp < 0 || bộMôTảTệp >= giớiHạnBộMôTả) return -9;
        return mởThẻXửLý[bộMôTảTệp] - 1;
    }
    static int bộMôTảRỗng(int chạy) {
        for (int sốHiệu = chạy; sốHiệu < giớiHạnBộMôTả; sốHiệu++) if (mởThẻXửLý[sốHiệu] == 0) return sốHiệu;
        return -24;
    }
    static int thẻXửLýRỗng() {
        for (int sốHiệu = 0; sốHiệu < giớiHạnBộMôTả; sốHiệu++) if (sốLượngThamChiếu[sốHiệu] == 0) return sốHiệu;
        return -24;
    }
    static int nốiKết(int mụcBộMôTả, int giáTrịBộMôTả, int loạiTệp, int giáTrịĐốiĐíchTệp, int cácThiếtLập) {
        mởThẻXửLý[mụcBộMôTả] = giáTrịBộMôTả + 1; đặtGiáTrịBộMôTả[mụcBộMôTả] = (cácThiếtLập & đóngThựcThiẢnhBậtTrạngThái) != 0 ? 1 : 0;
        giáTrịLoại[giáTrịBộMôTả] = loạiTệp; giáTrịĐốiĐích[giáTrịBộMôTả] = giáTrịĐốiĐíchTệp; sốLượngThamChiếu[giáTrịBộMôTả] = 1;
        mởCácThiếtLập[giáTrịBộMôTả] = cácThiếtLập & (3 | thêmCuốiSựTiếpDiễn | chờKhôngThựcHiện); vịTríTệp[giáTrịBộMôTả] = 0;
        thẻXửLýMạng[giáTrịBộMôTả] = 0; nhậnMiliGiâyHếtGiờ[giáTrịBộMôTả] = 0;
        return mụcBộMôTả;
    }
    static void bắtChạyTiếnTrình() {
        tiếnTrìnhSạch();
        for (int sốHiệu = 0; sốHiệu < 3; sốHiệu++) nốiKết(sốHiệu, sốHiệu, 1, sốHiệu, sốHiệu == 0 ? 0 : 1);
    }
    static void tiếnTrìnhSạch() {
        for (int sốHiệu = 0; sốHiệu < giớiHạnBộMôTả; sốHiệu++) if (mởThẻXửLý[sốHiệu] != 0) đóngTệp(sốHiệu);
    }
    static int đóngTệp(int mụcBộMôTả) {
        int giáTrịBộMôTả = tìmBộMôTả(mụcBộMôTả);
        if (giáTrịBộMôTả < 0) return -9;
        mởThẻXửLý[mụcBộMôTả] = 0; đặtGiáTrịBộMôTả[mụcBộMôTả] = 0;
        sốLượngThamChiếu[giáTrịBộMôTả]--;
        if (sốLượngThamChiếu[giáTrịBộMôTả] == 0) {
            if (giáTrịLoại[giáTrịBộMôTả] == 2) HệTệpBộNhớ.mởSốLượng[giáTrịĐốiĐích[giáTrịBộMôTả]]--;
            if (giáTrịLoại[giáTrịBộMôTả] == 3 && thẻXửLýMạng[giáTrịBộMôTả] != 0) NgănXếpMạng.đóng(thẻXửLýMạng[giáTrịBộMôTả]);
            giáTrịLoại[giáTrịBộMôTả] = 0;
        }
        return 0;
    }
    // Đường dẫn C là chuỗi byte kết thúc bằng NUL. Chỉ hỗ trợ một tên ngay dưới gốc.
    static int đọcĐườngDẫn(int địaChỉ) {
        if (!QuảnLýThựcThi.cắtXén(địaChỉ, 1)) return -14;
        int vịTrí = ThiếtBị.đọcBộNhớ(địaChỉ) == '/' ? 1 : 0;
        for (int độDài = 0; độDài < 64; độDài++) {
            if (!QuảnLýThựcThi.cắtXén(địaChỉ + vịTrí + độDài, 1)) return -14;
            int giáTrị = ThiếtBị.đọcBộNhớ(địaChỉ + vịTrí + độDài);
            tênĐườngDẫn[độDài] = giáTrị;
            if (giáTrị == 0) return độDài == 0 ? -2 : (HệTệpBộNhớ.kiểmTraTên(tênĐườngDẫn, độDài) ? độDài : -22);
            if (giáTrị == '/') return -20;
        }
        return -36;
    }
    static int mởTệp(int địaChỉTên, int cácThiếtLập, int cấpQuyềnQuyền) {
        int độDài = đọcĐườngDẫn(địaChỉTên);
        if (độDài < 0) return độDài;
        if ((cácThiếtLập & ~(3 | tạoMục | tạoRiêng | xóaSạchCácNộiDung | thêmCuốiSựTiếpDiễn | chờKhôngThựcHiện | đóngThựcThiẢnhBậtTrạngThái)) != 0) return -95;
        if ((cácThiếtLập & 3) == 3 || ((cácThiếtLập & xóaSạchCácNộiDung) != 0 && (cácThiếtLập & 3) == 0)) return -22;
        int Tệp = HệTệpBộNhớ.tìmMục(tênĐườngDẫn, độDài);
        if (Tệp >= 0 && (cácThiếtLập & (tạoMục | tạoRiêng)) == (tạoMục | tạoRiêng)) return -17;
        if (Tệp == -2 && (cácThiếtLập & tạoMục) == 0) return -2;
        int mụcBộMôTả = bộMôTảRỗng(0), giáTrịBộMôTả = thẻXửLýRỗng();
        if (mụcBộMôTả < 0 || giáTrịBộMôTả < 0) return -24;
        if (Tệp == -2) {
            int kếtQuả = HệTệpBộNhớ.giáTrịCất(tênĐườngDẫn, độDài, tênĐườngDẫn, 0);
            if (kếtQuả < 0) return kếtQuả;
            Tệp = HệTệpBộNhớ.tìmMục(tênĐườngDẫn, độDài);
            HệTệpBộNhớ.cácQuyềnĐượcCấpQuyền[Tệp] = cấpQuyềnQuyền & 511;
        }
        if (Tệp < 0) return Tệp;
        if ((cácThiếtLập & xóaSạchCácNộiDung) != 0) HệTệpBộNhớ.danhSáchCỡ[Tệp] = 0;
        HệTệpBộNhớ.mởSốLượng[Tệp]++;
        return nốiKết(mụcBộMôTả, giáTrịBộMôTả, 2, Tệp, cácThiếtLập);
    }
    static int đọcTệp(int mụcBộMôTả, int địaChỉDữLiệu, int độDài) {
        int giáTrịBộMôTả = tìmBộMôTả(mụcBộMôTả);
        if (giáTrịBộMôTả < 0 || (mởCácThiếtLập[giáTrịBộMôTả] & 3) == 1) return -9;
        if (độDài < 0) return -22;
        if (độDài == 0) return 0;
        if (!QuảnLýThựcThi.cắtXén(địaChỉDữLiệu, độDài)) return -14;
        if (giáTrịLoại[giáTrịBộMôTả] == 3) return nhậnDữLiệuĐiệnDữLiệu(mụcBộMôTả, địaChỉDữLiệu, độDài, 0, 0);
        if (giáTrịLoại[giáTrịBộMôTả] == 1) {
            int sốLượngĐãNhận = 0;
            while (sốLượngĐãNhận < độDài) {
                int giáTrị = ĐầuCuốiVănBản.đọcNốiTiếp();
                if (giáTrị < 0) giáTrị = BànPhím.đọc();
                if (giáTrị < 0) {
                    if (sốLượngĐãNhận > 0) return sốLượngĐãNhận;
                    if ((mởCácThiếtLập[giáTrịBộMôTả] & chờKhôngThựcHiện) != 0) return -11;
                    if (ThiếtBị.miliGiâyCònLạiNgườiDùng() <= 10) return -11;
                    NgănXếpMạng.xácMinh(); ThiếtBị.nhườngNgắn();
                } else {
                    ThiếtBị.ghiBộNhớ(địaChỉDữLiệu + sốLượngĐãNhận, giáTrị); sốLượngĐãNhận++;
                }
            }
            return sốLượngĐãNhận;
        }
        int Tệp = giáTrịĐốiĐích[giáTrịBộMôTả], vịTrí = vịTríTệp[giáTrịBộMôTả];
        if (vịTrí >= HệTệpBộNhớ.danhSáchCỡ[Tệp]) return 0;
        if (độDài > HệTệpBộNhớ.danhSáchCỡ[Tệp] - vịTrí) độDài = HệTệpBộNhớ.danhSáchCỡ[Tệp] - vịTrí;
        int địaChỉNguyênBản = ThiếtBị.bộNhớTệp() + Tệp * HệTệpBộNhớ.cỡTốiĐa + vịTrí;
        for (int sốHiệu = 0; sốHiệu < độDài; sốHiệu++) ThiếtBị.ghiBộNhớ(địaChỉDữLiệu + sốHiệu, ThiếtBị.đọcBộNhớ(địaChỉNguyênBản + sốHiệu));
        vịTríTệp[giáTrịBộMôTả] += độDài;
        return độDài;
    }
    static int ghiTệp(int mụcBộMôTả, int địaChỉDữLiệu, int độDài) {
        int giáTrịBộMôTả = tìmBộMôTả(mụcBộMôTả);
        if (giáTrịBộMôTả < 0 || (mởCácThiếtLập[giáTrịBộMôTả] & 3) == 0) return -9;
        if (độDài < 0) return -22;
        if (độDài == 0) return 0;
        if (!QuảnLýThựcThi.cắtXén(địaChỉDữLiệu, độDài)) return -14;
        if (giáTrịLoại[giáTrịBộMôTả] == 3) return -89; // Điểm cuối thông điệp chưa kết nối cần địa chỉ đích.
        if (giáTrịLoại[giáTrịBộMôTả] == 1) {
            if (độDài > 16384) độDài = 16384;
            for (int sốHiệu = 0; sốHiệu < độDài; sốHiệu++) {
                int giáTrị = ThiếtBị.đọcBộNhớ(địaChỉDữLiệu + sốHiệu);
                ĐầuCuốiVănBản.byteNốiTiếp(giáTrị); ĐầuCuốiVănBản.kýTựMànHình(giáTrị);
            }
            return độDài;
        }
        int Tệp = giáTrịĐốiĐích[giáTrịBộMôTả], cỡ = HệTệpBộNhớ.danhSáchCỡ[Tệp];
        int vịTrí = (mởCácThiếtLập[giáTrịBộMôTả] & thêmCuốiSựTiếpDiễn) != 0 ? cỡ : vịTríTệp[giáTrịBộMôTả];
        if (vịTrí >= HệTệpBộNhớ.cỡTốiĐa) return -27;
        if (độDài > HệTệpBộNhớ.cỡTốiĐa - vịTrí) độDài = HệTệpBộNhớ.cỡTốiĐa - vịTrí;
        int địaChỉĐích = ThiếtBị.bộNhớTệp() + Tệp * HệTệpBộNhớ.cỡTốiĐa;
        for (int sốHiệu = cỡ; sốHiệu < vịTrí; sốHiệu++) ThiếtBị.ghiBộNhớ(địaChỉĐích + sốHiệu, 0);
        for (int sốHiệu = 0; sốHiệu < độDài; sốHiệu++) ThiếtBị.ghiBộNhớ(địaChỉĐích + vịTrí + sốHiệu, ThiếtBị.đọcBộNhớ(địaChỉDữLiệu + sốHiệu));
        vịTríTệp[giáTrịBộMôTả] = vịTrí + độDài;
        if (vịTrí + độDài > cỡ) HệTệpBộNhớ.danhSáchCỡ[Tệp] = vịTrí + độDài;
        return độDài;
    }
    static int dịchVịTệp(int mụcBộMôTả, int giáTrịĐộLệch, int gốcCâyDựÁn) {
        int giáTrịBộMôTả = tìmBộMôTả(mụcBộMôTả);
        if (giáTrịBộMôTả < 0) return -9;
        if (giáTrịLoại[giáTrịBộMôTả] != 2) return -29;
        if (gốcCâyDựÁn < 0 || gốcCâyDựÁn > 2) return -22;
        int giáTrịNền = gốcCâyDựÁn == 0 ? 0 : (gốcCâyDựÁn == 1 ? vịTríTệp[giáTrịBộMôTả] : HệTệpBộNhớ.danhSáchCỡ[giáTrịĐốiĐích[giáTrịBộMôTả]]);
        if (giáTrịĐộLệch > 0 && giáTrịNền > 2147483647 - giáTrịĐộLệch) return -75;
        if (giáTrịĐộLệch < 0 && giáTrịĐộLệch < -giáTrịNền) return -22;
        vịTríTệp[giáTrịBộMôTả] = giáTrịNền + giáTrịĐộLệch;
        return vịTríTệp[giáTrịBộMôTả];
    }
    static int bộMôTảBảnSao(int mụcBộMôTả, int bộMôTảMới, boolean giáTrịGán, int cácThiếtLập) {
        int giáTrịBộMôTả = tìmBộMôTả(mụcBộMôTả);
        if (giáTrịBộMôTả < 0) return -9;
        if (bộMôTảMới < 0 || bộMôTảMới >= giớiHạnBộMôTả) return giáTrịGán ? -9 : -22;
        if (giáTrịGán && mụcBộMôTả == bộMôTảMới) return bộMôTảMới;
        if (giáTrịGán) { if (mởThẻXửLý[bộMôTảMới] != 0) đóngTệp(bộMôTảMới); }
        else { bộMôTảMới = bộMôTảRỗng(bộMôTảMới); if (bộMôTảMới < 0) return bộMôTảMới; }
        mởThẻXửLý[bộMôTảMới] = giáTrịBộMôTả + 1; đặtGiáTrịBộMôTả[bộMôTảMới] = cácThiếtLập; sốLượngThamChiếu[giáTrịBộMôTả]++;
        return bộMôTảMới;
    }
    static int gỡTênMụcTệp(int địaChỉTên) {
        int độDài = đọcĐườngDẫn(địaChỉTên);
        if (độDài < 0) return độDài;
        int Tệp = HệTệpBộNhớ.tìmMục(tênĐườngDẫn, độDài);
        if (Tệp < 0) return Tệp;
        HệTệpBộNhớ.danhSáchCácTên[Tệp * 64] = 0;
        return 0;
    }
    static int đặtGiáTrịĐộDàiTệp(int mụcBộMôTả, int độDài) {
        int giáTrịBộMôTả = tìmBộMôTả(mụcBộMôTả);
        if (giáTrịBộMôTả < 0) return -9;
        if (giáTrịLoại[giáTrịBộMôTả] != 2 || (mởCácThiếtLập[giáTrịBộMôTả] & 3) == 0 || độDài < 0) return -22;
        if (độDài > HệTệpBộNhớ.cỡTốiĐa) return -27;
        int Tệp = giáTrịĐốiĐích[giáTrịBộMôTả], địaChỉ = ThiếtBị.bộNhớTệp() + Tệp * HệTệpBộNhớ.cỡTốiĐa;
        for (int sốHiệu = HệTệpBộNhớ.danhSáchCỡ[Tệp]; sốHiệu < độDài; sốHiệu++) ThiếtBị.ghiBộNhớ(địaChỉ + sốHiệu, 0);
        HệTệpBộNhớ.danhSáchCỡ[Tệp] = độDài;
        return 0;
    }
    static int đọcTìnhTrạngTệp(int mụcBộMôTả, int địaChỉ) {
        int giáTrịBộMôTả = tìmBộMôTả(mụcBộMôTả);
        if (giáTrịBộMôTả < 0) return -9;
        if (!QuảnLýThựcThi.cắtXén(địaChỉ, 48)) return -14;
        for (int sốHiệu = 0; sốHiệu < 12; sốHiệu++) QuảnLýThựcThi.ghiSố(địaChỉ + sốHiệu * 4, 0);
        int Tệp = giáTrịĐốiĐích[giáTrịBộMôTả], cỡ = giáTrịLoại[giáTrịBộMôTả] == 2 ? HệTệpBộNhớ.danhSáchCỡ[Tệp] : 0;
        int cấpQuyềnQuyền = giáTrịLoại[giáTrịBộMôTả] == 2 ? HệTệpBộNhớ.cácQuyềnĐượcCấpQuyền[Tệp] : 438;
        QuảnLýThựcThi.ghiSố(địaChỉ, 1);
        QuảnLýThựcThi.ghiSố(địaChỉ + 4, giáTrịLoại[giáTrịBộMôTả] == 2 ? Tệp + 1 : 100 + giáTrịBộMôTả);
        QuảnLýThựcThi.ghiSố(địaChỉ + 8, (giáTrịLoại[giáTrịBộMôTả] == 2 ? 32768 : (giáTrịLoại[giáTrịBộMôTả] == 1 ? 8192 : 49152)) | cấpQuyềnQuyền);
        QuảnLýThựcThi.ghiSố(địaChỉ + 12, giáTrịLoại[giáTrịBộMôTả] == 2 && HệTệpBộNhớ.danhSáchCácTên[Tệp * 64] == 0 ? 0 : 1);
        QuảnLýThựcThi.ghiSố(địaChỉ + 28, cỡ); QuảnLýThựcThi.ghiSố(địaChỉ + 32, 512);
        QuảnLýThựcThi.ghiSố(địaChỉ + 36, (cỡ + 511) / 512);
        return 0;
    }
    static int bộMôTảĐiềuKhiển(int mụcBộMôTả, int lệnh, int giáTrị) {
        int giáTrịBộMôTả = tìmBộMôTả(mụcBộMôTả);
        if (giáTrịBộMôTả < 0) return -9;
        if (lệnh == 0 || lệnh == 1030) return bộMôTảBảnSao(mụcBộMôTả, giáTrị, false, lệnh == 1030 ? 1 : 0);
        if (lệnh == 1) return đặtGiáTrịBộMôTả[mụcBộMôTả];
        if (lệnh == 2) { if ((giáTrị & ~1) != 0) return -22; đặtGiáTrịBộMôTả[mụcBộMôTả] = giáTrị; return 0; }
        if (lệnh == 3) return mởCácThiếtLập[giáTrịBộMôTả];
        if (lệnh == 4) {
            if ((giáTrị & ~(3 | thêmCuốiSựTiếpDiễn | chờKhôngThựcHiện)) != 0) return -95;
            mởCácThiếtLập[giáTrịBộMôTả] = (mởCácThiếtLập[giáTrịBộMôTả] & 3) | (giáTrị & (thêmCuốiSựTiếpDiễn | chờKhôngThựcHiện)); return 0;
        }
        return -95;
    }
    static int tạoĐiểmCuối(int lượcĐồĐịaChỉ, int loạiMạng, int sốQuyƯớc) {
        if (lượcĐồĐịaChỉ != 2) return -97;
        if (loạiMạng != 2) return -93;
        if (sốQuyƯớc != 0 && sốQuyƯớc != 17) return -93;
        int mụcBộMôTả = bộMôTảRỗng(0), giáTrịBộMôTả = thẻXửLýRỗng();
        if (mụcBộMôTả < 0 || giáTrịBộMôTả < 0) return -24;
        return nốiKết(mụcBộMôTả, giáTrịBộMôTả, 3, 0, đọcCờGhi);
    }
    static int bộMôTảĐiểmCuối(int mụcBộMôTả) {
        int giáTrịBộMôTả = tìmBộMôTả(mụcBộMôTả);
        if (giáTrịBộMôTả < 0) return -9;
        return giáTrịLoại[giáTrịBộMôTả] == 3 ? giáTrịBộMôTả : -88;
    }
    static int địaChỉ32(int địaChỉ) {
        return ThiếtBị.đọcBộNhớ(địaChỉ) << 24 | ThiếtBị.đọcBộNhớ(địaChỉ + 1) << 16
            | ThiếtBị.đọcBộNhớ(địaChỉ + 2) << 8 | ThiếtBị.đọcBộNhớ(địaChỉ + 3);
    }
    static int kiểmTraĐịaChỉ(int địaChỉ, int độDài) {
        if (độDài < 16) return -22;
        if (!QuảnLýThựcThi.cắtXén(địaChỉ, 16)) return -14;
        return QuảnLýThựcThi.giáTrịNgắnKiểu(địaChỉ) == 2 ? 0 : -97;
    }
    static int ràngBuộcĐịaChỉ(int mụcBộMôTả, int địaChỉ, int độDài) {
        int giáTrịBộMôTả = bộMôTảĐiểmCuối(mụcBộMôTả);
        if (giáTrịBộMôTả < 0) return giáTrịBộMôTả;
        int kếtQuả = kiểmTraĐịaChỉ(địaChỉ, độDài);
        if (kếtQuả < 0) return kếtQuả;
        if (thẻXửLýMạng[giáTrịBộMôTả] != 0) return -22;
        int địaChỉMạng = địaChỉ32(địaChỉ + 4);
        if (địaChỉMạng != 0 && địaChỉMạng != NgănXếpMạng.địaChỉTựCó) return -99;
        int sốCổng = ThiếtBị.đọcBộNhớ(địaChỉ + 2) << 8 | ThiếtBị.đọcBộNhớ(địaChỉ + 3);
        kếtQuả = NgănXếpMạng.mở(sốCổng);
        if (kếtQuả < 0) return kếtQuả;
        thẻXửLýMạng[giáTrịBộMôTả] = kếtQuả; giáTrịĐốiĐích[giáTrịBộMôTả] = địaChỉMạng;
        return 0;
    }
    static int ràngBuộcTựĐộng(int giáTrịBộMôTả) {
        if (thẻXửLýMạng[giáTrịBộMôTả] != 0) return 0;
        int kếtQuả = NgănXếpMạng.mở(0);
        if (kếtQuả < 0) return kếtQuả;
        thẻXửLýMạng[giáTrịBộMôTả] = kếtQuả;
        return 0;
    }
    // Hai đối số cuối của sendto/recvfrom được truyền trong cấu trúc yêu cầu 8 byte.
    static int gửiDữLiệuĐiệnDữLiệu(int mụcBộMôTả, int địaChỉDữLiệu, int độDài, int cácThiếtLập, int địaChỉĐãYêuCầu) {
        int giáTrịBộMôTả = bộMôTảĐiểmCuối(mụcBộMôTả);
        if (giáTrịBộMôTả < 0) return giáTrịBộMôTả;
        if (cácThiếtLập != 0) return -95;
        if (độDài < 0 || độDài > 1024) return -90;
        if (độDài != 0 && !QuảnLýThựcThi.cắtXén(địaChỉDữLiệu, độDài)) return -14;
        if (!QuảnLýThựcThi.cắtXén(địaChỉĐãYêuCầu, 8)) return -14;
        int địaChỉ = QuảnLýThựcThi.trịSố(địaChỉĐãYêuCầu);
        int kếtQuả = kiểmTraĐịaChỉ(địaChỉ, QuảnLýThựcThi.trịSố(địaChỉĐãYêuCầu + 4));
        if (kếtQuả < 0) return kếtQuả;
        int sốCổng = ThiếtBị.đọcBộNhớ(địaChỉ + 2) << 8 | ThiếtBị.đọcBộNhớ(địaChỉ + 3);
        if (sốCổng == 0) return -22;
        kếtQuả = ràngBuộcTựĐộng(giáTrịBộMôTả);
        if (kếtQuả < 0) return kếtQuả;
        for (int sốHiệu = 0; sốHiệu < độDài; sốHiệu++) dữLiệuChuyểnGiao[sốHiệu] = ThiếtBị.đọcBộNhớ(địaChỉDữLiệu + sốHiệu);
        return NgănXếpMạng.gửi(thẻXửLýMạng[giáTrịBộMôTả], địaChỉ32(địaChỉ + 4), sốCổng, dữLiệuChuyểnGiao, độDài);
    }
    static void ghiĐịaChỉ(int địaChỉ, int độDài, int địaChỉMạng, int sốCổng) {
        for (int sốHiệu = 0; sốHiệu < độDài && sốHiệu < 16; sốHiệu++) {
            int giáTrị = 0;
            if (sốHiệu == 0) giáTrị = 2;
            if (sốHiệu == 2) giáTrị = sốCổng >>> 8;
            if (sốHiệu == 3) giáTrị = sốCổng;
            if (sốHiệu >= 4 && sốHiệu < 8) giáTrị = địaChỉMạng >>> (56 - sốHiệu * 8);
            ThiếtBị.ghiBộNhớ(địaChỉ + sốHiệu, giáTrị & 255);
        }
    }
    static int nhậnDữLiệuĐiệnDữLiệu(int mụcBộMôTả, int địaChỉDữLiệu, int độDài, int cácThiếtLập, int địaChỉĐãYêuCầu) {
        int giáTrịBộMôTả = bộMôTảĐiểmCuối(mụcBộMôTả);
        if (giáTrịBộMôTả < 0) return giáTrịBộMôTả;
        if ((cácThiếtLập & ~64) != 0) return -95;
        if (độDài < 0) return -22;
        if (độDài != 0 && !QuảnLýThựcThi.cắtXén(địaChỉDữLiệu, độDài)) return -14;
        int địaChỉ = 0, địaChỉĐộDàiĐịaChỉ = 0, độDàiĐịaChỉ = 0;
        if (địaChỉĐãYêuCầu != 0) {
            if (!QuảnLýThựcThi.cắtXén(địaChỉĐãYêuCầu, 8)) return -14;
            địaChỉ = QuảnLýThựcThi.trịSố(địaChỉĐãYêuCầu); địaChỉĐộDàiĐịaChỉ = QuảnLýThựcThi.trịSố(địaChỉĐãYêuCầu + 4);
            if (địaChỉ != 0) {
                if (!QuảnLýThựcThi.cắtXén(địaChỉĐộDàiĐịaChỉ, 4)) return -14;
                độDàiĐịaChỉ = QuảnLýThựcThi.trịSố(địaChỉĐộDàiĐịaChỉ);
                if (độDàiĐịaChỉ < 0) return -22;
                if (!QuảnLýThựcThi.cắtXén(địaChỉ, độDàiĐịaChỉ < 16 ? độDàiĐịaChỉ : 16)) return -14;
            }
        }
        int kếtQuả = ràngBuộcTựĐộng(giáTrịBộMôTả);
        if (kếtQuả < 0) return kếtQuả;
        int chạy = ThiếtBị.miliGiây();
        while (true) {
            kếtQuả = NgănXếpMạng.nhận(thẻXửLýMạng[giáTrịBộMôTả], dữLiệuChuyểnGiao, 1024, 0);
            if (kếtQuả != -11) break;
            if ((cácThiếtLập & 64) != 0 || (mởCácThiếtLập[giáTrịBộMôTả] & chờKhôngThựcHiện) != 0) return -11;
            if (nhậnMiliGiâyHếtGiờ[giáTrịBộMôTả] > 0 && ThiếtBị.miliGiây() - chạy >= nhậnMiliGiâyHếtGiờ[giáTrịBộMôTả]) return -11;
            if (ThiếtBị.miliGiâyCònLạiNgườiDùng() <= 10) return -11;
            ThiếtBị.nhườngNgắn();
        }
        if (kếtQuả < 0) return kếtQuả;
        if (kếtQuả > độDài) kếtQuả = độDài;
        for (int sốHiệu = 0; sốHiệu < kếtQuả; sốHiệu++) ThiếtBị.ghiBộNhớ(địaChỉDữLiệu + sốHiệu, dữLiệuChuyểnGiao[sốHiệu]);
        if (địaChỉ != 0) {
            ghiĐịaChỉ(địaChỉ, độDàiĐịaChỉ, NgănXếpMạng.địaChỉĐốiTác(thẻXửLýMạng[giáTrịBộMôTả]), NgănXếpMạng.sốCổngĐốiTác(thẻXửLýMạng[giáTrịBộMôTả]));
            QuảnLýThựcThi.ghiSố(địaChỉĐộDàiĐịaChỉ, 16);
        }
        return kếtQuả;
    }
    static int đọcĐịaChỉỔCắmMạng(int mụcBộMôTả, int địaChỉ, int địaChỉĐộDài) {
        int giáTrịBộMôTả = bộMôTảĐiểmCuối(mụcBộMôTả);
        if (giáTrịBộMôTả < 0) return giáTrịBộMôTả;
        if (!QuảnLýThựcThi.cắtXén(địaChỉĐộDài, 4)) return -14;
        int độDài = QuảnLýThựcThi.trịSố(địaChỉĐộDài);
        if (độDài < 0) return -22;
        if (!QuảnLýThựcThi.cắtXén(địaChỉ, độDài < 16 ? độDài : 16)) return -14;
        int mụcÔ = NgănXếpMạng.sốHiệu(thẻXửLýMạng[giáTrịBộMôTả]);
        ghiĐịaChỉ(địaChỉ, độDài, giáTrịĐốiĐích[giáTrịBộMôTả], mụcÔ < 0 ? 0 : NgănXếpMạng.cácCổng[mụcÔ]);
        QuảnLýThựcThi.ghiSố(địaChỉĐộDài, 16);
        return 0;
    }
    static int đặtGiáTrịHếtGiờNhận(int mụcBộMôTả, int miliGiây) {
        int giáTrịBộMôTả = bộMôTảĐiểmCuối(mụcBộMôTả);
        if (giáTrịBộMôTả < 0) return giáTrịBộMôTả;
        if (miliGiây < 0 || miliGiây > 2000) return -22;
        nhậnMiliGiâyHếtGiờ[giáTrịBộMôTả] = miliGiây;
        return 0;
    }
}
