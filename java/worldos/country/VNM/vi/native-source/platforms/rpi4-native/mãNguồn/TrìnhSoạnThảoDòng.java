// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Chèn, xóa, phím mũi tên, lịch sử lệnh và hoàn tất bằng Tab đều giữ ranh giới byte UTF-8. */
public final class TrìnhSoạnThảoDòng {
    static boolean dòngLệnh;
    static int[] bảnGhiNhậtKý = new int[16 * 1024], độDàiNhậtKý = new int[16], giáTrịCất = new int[4096], ứngViên = new int[64];
    static int sốLượngNhậtKý, kếtThúcBảnGhiNhậtKý, tìmKiếmGiáTrị, độDàiĐãCất, cỡ, giáTrịConTrỏVănBản, sốLượngỨngViên, độDàiỨngViên, bắtChạyCửaSổ;
    static boolean hiệnVịTríNgang;
    static String danhSáchCácLệnh = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd vỏLệnhAnToàn HiểnThịTừXa run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] ứngViênLệnh = new int[128];
    static void thêmỨngViênLệnh(String danhSáchMục, int bắtChạyVịTrí, int vịTríKếtThúc, int độDàiĐầuVào) {
        int sốLượngByte=0;
        for(int chỉSốVịTrí=bắtChạyVịTrí;chỉSốVịTrí<vịTríKếtThúc;chỉSốVịTrí++) {
            int mãKýTự=danhSáchMục.charAt(chỉSốVịTrí);
            if(mãKýTự>=0xd800 && mãKýTự<=0xdbff && chỉSốVịTrí+1<vịTríKếtThúc)mãKýTự=0x10000+((mãKýTự-0xd800)<<10)+danhSáchMục.charAt(++chỉSốVịTrí)-0xdc00;
            int trịSố=mãKýTự<128?1:mãKýTự<2048?2:mãKýTự<65536?3:4;
            if(sốLượngByte+trịSố>62)return;
            for(int giáTrịDãy=trịSố-1;giáTrịDãy>=0;giáTrịDãy--)ứngViênLệnh[sốLượngByte++]=trịSố==1?mãKýTự:giáTrịDãy==trịSố-1?(trịSố==2?0xc0:trịSố==3?0xe0:0xf0)|(mãKýTự>>(6*giáTrịDãy)):0x80|((mãKýTự>>(6*giáTrịDãy))&63);
        }
        if(sốLượngByte<độDàiĐầuVào)return;
        for(int chỉSốVịTrí=0;chỉSốVịTrí<độDàiĐầuVào;chỉSốVịTrí++)if(ứngViênLệnh[chỉSốVịTrí]!=TrìnhThôngDịchLệnh.dòng[chỉSốVịTrí])return;
        sốLượngỨngViên++;độDàiỨngViên=sốLượngByte+1;
        for(int chỉSốVịTrí=0;chỉSốVịTrí<sốLượngByte;chỉSốVịTrí++)ứngViên[chỉSốVịTrí]=ứngViênLệnh[chỉSốVịTrí];ứngViên[sốLượngByte]=' ';
    }
    static int giáTrịPhíaTrước(int đọcConTrỏVănBản) { if (đọcConTrỏVănBản > 0) { đọcConTrỏVănBản--; while (đọcConTrỏVănBản > 0 && (TrìnhThôngDịchLệnh.dòng[đọcConTrỏVănBản] & 192) == 128) đọcConTrỏVănBản--; } return đọcConTrỏVănBản; }
    static int giáTrịLùi(int đọcConTrỏVănBản) { if (đọcConTrỏVănBản < cỡ) { đọcConTrỏVănBản++; while (đọcConTrỏVănBản < cỡ && (TrìnhThôngDịchLệnh.dòng[đọcConTrỏVănBản] & 192) == 128) đọcConTrỏVănBản++; } return đọcConTrỏVănBản; }
    static int khoảngTrảiRộng(int bắtChạyVịTrí, int chỉSốGiáTrịĐích) {
        int cácÔ = 0;
        for (int chỉSốVòngLặp = bắtChạyVịTrí; chỉSốVòngLặp < chỉSốGiáTrịĐích; chỉSốVòngLặp++) { int dữLiệuByte = TrìnhThôngDịchLệnh.dòng[chỉSốVòngLặp]; if ((dữLiệuByte & 192) == 128) continue; cácÔ += dữLiệuByte >= 196 ? 2 : 1; }
        return cácÔ;
    }
    static void giáTrịThửLại() {
        VàoRaThiếtBịCuối.ghi("\r\u001b[2K");
        VàoRaThiếtBịCuối.ghi(dòngLệnh ? "jkoros-native> " : "edit> ");
        cácDòngHiệnĐược();
    }
    // Di chuyển ngang trong một dòng vật lý. Hiển thị lại lệnh dài không được xóa phần đầu ra phía trên.
    static int rộngHiệnĐược() { int cácCột = BoMạch.thiếtBịCuối(13) & 65535; return cácCột - (dòngLệnh ? 18 : 9); }
    static void cácDòngHiệnĐược() {
        if (giáTrịConTrỏVănBản < bắtChạyCửaSổ) bắtChạyCửaSổ = giáTrịConTrỏVănBản;
        while (khoảngTrảiRộng(bắtChạyCửaSổ, giáTrịConTrỏVănBản) > rộngHiệnĐược()) bắtChạyCửaSổ = giáTrịLùi(bắtChạyCửaSổ);
        int vịTríKếtThúc = bắtChạyCửaSổ;
        while (vịTríKếtThúc < cỡ && khoảngTrảiRộng(bắtChạyCửaSổ, giáTrịLùi(vịTríKếtThúc)) <= rộngHiệnĐược()) vịTríKếtThúc = giáTrịLùi(vịTríKếtThúc);
        VàoRaThiếtBịCuối.ghi("\r\u001b["); VàoRaThiếtBịCuối.trịSố(dòngLệnh ? 16 : 7); VàoRaThiếtBịCuối.ghi("G\u001b[K");
        if (bắtChạyCửaSổ > 0) VàoRaThiếtBịCuối.KýTự('<');
        for (int chỉSốVòngLặp = bắtChạyCửaSổ; chỉSốVòngLặp < vịTríKếtThúc; chỉSốVòngLặp++) BoMạch.ghiNốiTiếp(TrìnhThôngDịchLệnh.dòng[chỉSốVòngLặp]);
        VàoRaThiếtBịCuối.KýTự(vịTríKếtThúc < cỡ ? '>' : ' ');
        VàoRaThiếtBịCuối.ghi("\u001b["); VàoRaThiếtBịCuối.trịSố(khoảngTrảiRộng(giáTrịConTrỏVănBản, vịTríKếtThúc) + 1); VàoRaThiếtBịCuối.KýTự('D');
        hiệnVịTríNgang = bắtChạyCửaSổ > 0 || vịTríKếtThúc < cỡ || khoảngTrảiRộng(0, cỡ) > rộngHiệnĐược();
    }
    static void thêmCuốiNhậtKý() {
        if (!dòngLệnh || cỡ == 0 || cỡ > 1024) return;
        if (sốLượngNhậtKý > 0) {
            int vịTríCuối = (kếtThúcBảnGhiNhậtKý + 15) % 16; boolean làGiốngNhau = độDàiNhậtKý[vịTríCuối] == cỡ;
            for (int chỉSốVòngLặp = 0; làGiốngNhau && chỉSốVòngLặp < cỡ; chỉSốVòngLặp++) if (bảnGhiNhậtKý[vịTríCuối * 1024 + chỉSốVòngLặp] != TrìnhThôngDịchLệnh.dòng[chỉSốVòngLặp]) làGiốngNhau = false;
            if (làGiốngNhau) return;
        }
        độDàiNhậtKý[kếtThúcBảnGhiNhậtKý] = cỡ; for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < cỡ; chỉSốVòngLặp++) bảnGhiNhậtKý[kếtThúcBảnGhiNhậtKý * 1024 + chỉSốVòngLặp] = TrìnhThôngDịchLệnh.dòng[chỉSốVòngLặp];
        kếtThúcBảnGhiNhậtKý = (kếtThúcBảnGhiNhậtKý + 1) % 16; if (sốLượngNhậtKý < 16) sốLượngNhậtKý++;
    }
    static void chuyểnĐộngNhậtKý(int giáTrịĐộChênh) {
        if (!dòngLệnh) return;
        if (tìmKiếmGiáTrị == 0 && giáTrịĐộChênh > 0) { độDàiĐãCất = cỡ; for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < cỡ; chỉSốVòngLặp++) giáTrịCất[chỉSốVòngLặp] = TrìnhThôngDịchLệnh.dòng[chỉSốVòngLặp]; }
        int vịTríKếTiếp = tìmKiếmGiáTrị + giáTrịĐộChênh; if (vịTríKếTiếp < 0 || vịTríKếTiếp > sốLượngNhậtKý) return; tìmKiếmGiáTrị = vịTríKếTiếp;
        if (tìmKiếmGiáTrị == 0) { cỡ = độDàiĐãCất; for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < cỡ; chỉSốVòngLặp++) TrìnhThôngDịchLệnh.dòng[chỉSốVòngLặp] = giáTrịCất[chỉSốVòngLặp]; }
        else { int ôĐãGiữNguyên = (kếtThúcBảnGhiNhậtKý + 16 - tìmKiếmGiáTrị) % 16; cỡ = độDàiNhậtKý[ôĐãGiữNguyên]; for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < cỡ; chỉSốVòngLặp++) TrìnhThôngDịchLệnh.dòng[chỉSốVòngLặp] = bảnGhiNhậtKý[ôĐãGiữNguyên * 1024 + chỉSốVòngLặp]; }
        giáTrịConTrỏVănBản = cỡ; giáTrịThửLại();
    }
    static void hiệnNhậtKý() {
        for (int sốLượngMục = 0; sốLượngMục < sốLượngNhậtKý; sốLượngMục++) {
            int ôĐãGiữNguyên = (kếtThúcBảnGhiNhậtKý + 16 - sốLượngNhậtKý + sốLượngMục) % 16; VàoRaThiếtBịCuối.trịSố(sốLượngMục + 1); VàoRaThiếtBịCuối.ghi("  ");
            for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < độDàiNhậtKý[ôĐãGiữNguyên]; chỉSốVòngLặp++) BoMạch.ghiNốiTiếp(bảnGhiNhậtKý[ôĐãGiữNguyên * 1024 + chỉSốVòngLặp]); VàoRaThiếtBịCuối.KýTự(10);
        }
    }
    static void thêmỨngViên(int[] mảngDữLiệu, int bắtChạyVịTrí, int sốLượngMục, int tiềnTố, int sốLượngTổngCộng, boolean sốThưMục) {
        if (sốLượngMục < sốLượngTổngCộng || sốLượngMục > 62) return;
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < sốLượngTổngCộng; chỉSốVòngLặp++) if (mảngDữLiệu[bắtChạyVịTrí + chỉSốVòngLặp] != TrìnhThôngDịchLệnh.dòng[tiềnTố + chỉSốVòngLặp]) return;
        sốLượngỨngViên++; độDàiỨngViên = sốLượngMục + 1;
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < sốLượngMục; chỉSốVòngLặp++) ứngViên[chỉSốVòngLặp] = mảngDữLiệu[bắtChạyVịTrí + chỉSốVòngLặp]; ứngViên[sốLượngMục] = sốThưMục ? '/' : ' ';
    }
    static void giáTrịĐãHoànTất() {
        if (!dòngLệnh || giáTrịConTrỏVănBản != cỡ) return;
        int điểmĐangBắtChạy = cỡ; while (điểmĐangBắtChạy > 0 && TrìnhThôngDịchLệnh.dòng[điểmĐangBắtChạy - 1] != ' ') điểmĐangBắtChạy--;
        for (int chỉSốVòngLặp = điểmĐangBắtChạy; chỉSốVòngLặp < cỡ; chỉSốVòngLặp++) if (TrìnhThôngDịchLệnh.dòng[chỉSốVòngLặp] == '/' || TrìnhThôngDịchLệnh.dòng[chỉSốVòngLặp] == '"' || TrìnhThôngDịchLệnh.dòng[chỉSốVòngLặp] == 39 || TrìnhThôngDịchLệnh.dòng[chỉSốVòngLặp] == '\\') return;
        sốLượngỨngViên = 0; int sốLượngMục = cỡ - điểmĐangBắtChạy;
        if (điểmĐangBắtChạy == 0) {
            for(int chỉSốDanhSách=0;chỉSốDanhSách<2;chỉSốDanhSách++) {
                String danhSáchMục=chỉSốDanhSách==0?danhSáchCácLệnh:LệnhQuảnTrị.từĐãHoànTất();
                int đọcConTrỏVănBản=0;
                while(đọcConTrỏVănBản<danhSáchMục.length()) {
                    int vịTríKếtThúc=đọcConTrỏVănBản;while(vịTríKếtThúc<danhSáchMục.length() && danhSáchMục.charAt(vịTríKếtThúc)!=' ')vịTríKếtThúc++;
                    thêmỨngViênLệnh(danhSáchMục,đọcConTrỏVănBản,vịTríKếtThúc,sốLượngMục);đọcConTrỏVănBản=vịTríKếtThúc+1;
                }
            }
        } else {
            CácTệpBộNhớ.bắtChạyĐườngDẫn(1); CácTệpBộNhớ.byteĐườngDẫn(0, '.'); CácTệpBộNhớ.chuẩnHóaGiáTrị();
            for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < CácTệpBộNhớ.sốLượngTệp; chỉSốVòngLặp++) {
                int bắtChạyVịTrí = CácTệpBộNhớ.bắtChạyMục(CácTệpBộNhớ.tên, chỉSốVòngLặp * 64, CácTệpBộNhớ.độDàiTên[chỉSốVòngLặp]);
                if (bắtChạyVịTrí >= 0) thêmỨngViên(CácTệpBộNhớ.tên, chỉSốVòngLặp * 64 + bắtChạyVịTrí, CácTệpBộNhớ.độDàiTên[chỉSốVòngLặp] - bắtChạyVịTrí, điểmĐangBắtChạy, sốLượngMục, false);
            }
            for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < 16; chỉSốVòngLặp++) {
                int bắtChạyVịTrí = CácTệpBộNhớ.bắtChạyMục(CácTệpBộNhớ.tênThưMục, chỉSốVòngLặp * 64, CácTệpBộNhớ.độDàiThưMục[chỉSốVòngLặp]);
                if (bắtChạyVịTrí >= 0) thêmỨngViên(CácTệpBộNhớ.tênThưMục, chỉSốVòngLặp * 64 + bắtChạyVịTrí, CácTệpBộNhớ.độDàiThưMục[chỉSốVòngLặp] - bắtChạyVịTrí, điểmĐangBắtChạy, sốLượngMục, true);
            }
        }
        if (sốLượngỨngViên != 1) { BoMạch.ghiNốiTiếp(7); return; }
        for (int chỉSốVòngLặp = sốLượngMục; chỉSốVòngLặp < độDàiỨngViên && cỡ < TrìnhThôngDịchLệnh.dòng.length - 1; chỉSốVòngLặp++) {
            if (ứngViên[chỉSốVòngLặp] == ' ' && chỉSốVòngLặp != độDàiỨngViên - 1) TrìnhThôngDịchLệnh.dòng[cỡ++] = '\\';
            TrìnhThôngDịchLệnh.dòng[cỡ++] = ứngViên[chỉSốVòngLặp];
        }
        giáTrịConTrỏVănBản = cỡ; giáTrịThửLại();
    }
    static int đọcThoát() {
        int điểmĐangBắtChạy = BoMạch.miliGiây();
        while (BoMạch.miliGiây() - điểmĐangBắtChạy < 80) { int dữLiệuByte = BoMạch.đọcNốiTiếp(); if (dữLiệuByte >= 0) return dữLiệuByte; BoMạch.nhườngBộXửLýTrungTâm(); }
        return -1;
    }
    static void giáTrịThoát() {
        int đầuTiên = đọcThoát(); if (đầuTiên != '[' && đầuTiên != 'O') return;
        int sốLượngMục = 0, vịTríKếtThúc = -1;
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < 12; chỉSốVòngLặp++) { int dữLiệuByte = đọcThoát(); if (dữLiệuByte < 0) return; if (dữLiệuByte >= '0' && dữLiệuByte <= '9') sốLượngMục = sốLượngMục * 10 + dữLiệuByte - '0'; else { vịTríKếtThúc = dữLiệuByte; break; } }
        if (vịTríKếtThúc == 'A') chuyểnĐộngNhậtKý(1);
        else if (vịTríKếtThúc == 'B') chuyểnĐộngNhậtKý(-1);
        else if (vịTríKếtThúc == 'C') { giáTrịConTrỏVănBản = giáTrịLùi(giáTrịConTrỏVănBản); giáTrịThửLại(); }
        else if (vịTríKếtThúc == 'D') { giáTrịConTrỏVănBản = giáTrịPhíaTrước(giáTrịConTrỏVănBản); giáTrịThửLại(); }
        else if (vịTríKếtThúc == 'H' || vịTríKếtThúc == '~' && (sốLượngMục == 1 || sốLượngMục == 7)) { giáTrịConTrỏVănBản = 0; giáTrịThửLại(); }
        else if (vịTríKếtThúc == 'F' || vịTríKếtThúc == '~' && (sốLượngMục == 4 || sốLượngMục == 8)) { giáTrịConTrỏVănBản = cỡ; giáTrịThửLại(); }
        else if (vịTríKếtThúc == '~' && sốLượngMục == 3 && giáTrịConTrỏVănBản < cỡ) {
            int vịTríKếTiếp = giáTrịLùi(giáTrịConTrỏVănBản); for (int chỉSốVòngLặp = vịTríKếTiếp; chỉSốVòngLặp < cỡ; chỉSốVòngLặp++) TrìnhThôngDịchLệnh.dòng[chỉSốVòngLặp - vịTríKếTiếp + giáTrịConTrỏVănBản] = TrìnhThôngDịchLệnh.dòng[chỉSốVòngLặp]; cỡ -= vịTríKếTiếp - giáTrịConTrỏVănBản; giáTrịThửLại();
        }
        else if (vịTríKếtThúc == '~' && (sốLượngMục == 5 || sốLượngMục == 6)) BoMạch.thiếtBịCuối(sốLượngMục == 5 ? 5 : 6);
        else if (vịTríKếtThúc == '~' && sốLượngMục == 24 && dòngLệnh) { TrìnhThôngDịchLệnh.thiếtBịCuối(true); }
    }
    static int đọc() {
        if (!phiênCửaSổ.đọcSựTiếpDiễn) { cỡ = giáTrịConTrỏVănBản = tìmKiếmGiáTrị = bắtChạyCửaSổ = 0; hiệnVịTríNgang = false; }
        else { phiênCửaSổ.đọcSựTiếpDiễn = false; giáTrịThửLại(); } boolean tràn = false;
        while (true) {
            int dữLiệuByte = BoMạch.đọcNốiTiếp(); if (dữLiệuByte == -4096) return -3;
            if (BoMạch.thiếtBịCuối(14) != 0) giáTrịThửLại(); if (dữLiệuByte < 0) { BoMạch.nhườngBộXửLýTrungTâm(); continue; }
            if (dữLiệuByte == 10 && TrìnhThôngDịchLệnh.dòngTrướcĐó) { TrìnhThôngDịchLệnh.dòngTrướcĐó = false; continue; } TrìnhThôngDịchLệnh.dòngTrướcĐó = dữLiệuByte == 13;
            if (dữLiệuByte == 27) { giáTrịThoát(); continue; }
            if (dữLiệuByte == 3) { VàoRaThiếtBịCuối.ghi("^C\n"); return -1; }
            if (dữLiệuByte == 4 && cỡ == 0 && dòngLệnh) { if (BoMạch.thiếtBịCuối(2) != 0) TrìnhThôngDịchLệnh.thiếtBịCuối(true); return -1; }
            if (dữLiệuByte == 13 || dữLiệuByte == 10) { VàoRaThiếtBịCuối.KýTự(10); if (!tràn) thêmCuốiNhậtKý(); return tràn ? -2 : cỡ; }
            if (dữLiệuByte == 9 && dòngLệnh) { giáTrịĐãHoànTất(); continue; }
            if (dữLiệuByte == 1 || dữLiệuByte == 5) { giáTrịConTrỏVănBản = dữLiệuByte == 1 ? 0 : cỡ; giáTrịThửLại(); continue; }
            if (dữLiệuByte == 8 || dữLiệuByte == 127 || dữLiệuByte == 21) {
                if (dữLiệuByte == 21) { for (int chỉSốVòngLặp = giáTrịConTrỏVănBản; chỉSốVòngLặp < cỡ; chỉSốVòngLặp++) TrìnhThôngDịchLệnh.dòng[chỉSốVòngLặp - giáTrịConTrỏVănBản] = TrìnhThôngDịchLệnh.dòng[chỉSốVòngLặp]; cỡ -= giáTrịConTrỏVănBản; giáTrịConTrỏVănBản = 0; }
                else if (giáTrịConTrỏVănBản > 0) { int đổiTrướcKhi = giáTrịPhíaTrước(giáTrịConTrỏVănBản); for (int chỉSốVòngLặp = giáTrịConTrỏVănBản; chỉSốVòngLặp < cỡ; chỉSốVòngLặp++) TrìnhThôngDịchLệnh.dòng[chỉSốVòngLặp - giáTrịConTrỏVănBản + đổiTrướcKhi] = TrìnhThôngDịchLệnh.dòng[chỉSốVòngLặp]; cỡ -= giáTrịConTrỏVănBản - đổiTrướcKhi; giáTrịConTrỏVănBản = đổiTrướcKhi; }
                giáTrịThửLại(); continue;
            }
            if (dữLiệuByte == 11) { cỡ = giáTrịConTrỏVănBản; giáTrịThửLại(); continue; }
            if (dữLiệuByte < 32 && dữLiệuByte != 9) continue;
            if (cỡ == TrìnhThôngDịchLệnh.dòng.length) { tràn = true; continue; }
            for (int chỉSốVòngLặp = cỡ; chỉSốVòngLặp > giáTrịConTrỏVănBản; chỉSốVòngLặp--) TrìnhThôngDịchLệnh.dòng[chỉSốVòngLặp] = TrìnhThôngDịchLệnh.dòng[chỉSốVòngLặp - 1];
            TrìnhThôngDịchLệnh.dòng[giáTrịConTrỏVănBản++] = dữLiệuByte; cỡ++;
            if (giáTrịConTrỏVănBản == cỡ && !hiệnVịTríNgang && khoảngTrảiRộng(0, cỡ) <= rộngHiệnĐược()) BoMạch.ghiNốiTiếp(dữLiệuByte);
            else if (giáTrịConTrỏVănBản == cỡ) cácDòngHiệnĐược(); else giáTrịThửLại();
        }
    }
}
