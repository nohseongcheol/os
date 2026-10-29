// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Bản chuyển ban đầu sang Pi4 của nhân Java độc lập; không chạy trên Linux hay JVM của máy chủ. */
public final class Nhân {
    static int[] cácLầnLặpTácVụ = new int[3];
    static int[] tổngTácVụ = new int[3];
    static int thứTựTácVụ;
    static int lỗiTácVụ;
    static int hạtGiốngNgẫuNhiên = 17;

    static void xácMinh(boolean điềuKiện, int sốHiệu) {
        if (!điềuKiện) { VàoRaThiếtBịCuối.ghi("FAIL "); VàoRaThiếtBịCuối.trịSố(sốHiệu); BoMạch.dừng(sốHiệu); }
    }
    static int nhánh(int giáTrị) {
        switch (giáTrị) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int chuyểnDày(int giáTrị) {
        switch (giáTrị) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] mảngTrảVề(int[] giáTrịMảng) { return giáTrịMảng; }
    static void thửSốHọc() {
        int giáTrị = hạtGiốngNgẫuNhiên;
        xácMinh(giáTrị * 7 - giáTrị == 102 && giáTrị / 3 == 5 && giáTrị % 3 == 2, 1);
        int sốNguyênTốiThiểu = 0x80000000, mộtÂm = -1;
        xácMinh(sốNguyênTốiThiểu / mộtÂm == sốNguyênTốiThiểu && sốNguyênTốiThiểu % mộtÂm == 0, 2);
        xácMinh(sốNguyênTốiThiểu + sốNguyênTốiThiểu == 0 && -sốNguyênTốiThiểu == sốNguyênTốiThiểu, 3);
        xácMinh((-giáTrị >> 2) == -5 && (-giáTrị >>> 2) == 1073741819 && (giáTrị << 33) == 34, 4);
        xácMinh((byte)(giáTrị * 16) == 16 && (short)65535 == -1 && (char)mộtÂm == 65535, 5);
        int[] giáTrịMảng = new int[5];
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < giáTrịMảng.length; chỉSốVòngLặp++) giáTrịMảng[chỉSốVòngLặp] = chỉSốVòngLặp * giáTrị;
        giáTrịMảng[2]++;
        xácMinh(mảngTrảVề(giáTrịMảng) == giáTrịMảng && giáTrịMảng[2] == 35 && giáTrịMảng[4] == 68, 6);
        xácMinh(nhánh(giáTrị - 117) == 7 && nhánh(giáTrị - 15) == 9 && nhánh(giáTrị) == 3 && chuyểnDày(giáTrị - 15) == 17, 7);
        String vănBản = "한글 😀";
        xácMinh(vănBản.length() == 5 && vănBản.charAt(0) == '한' && vănBản.charAt(3) == 0xd83d, 8);
        xácMinh(BoMạch.mứcĐặcQuyềnCPU() == 1, 9);
        VàoRaThiếtBịCuối.ghi("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void TácVụ(int sốHiệu) {
        // Kiểm tra biến cục bộ được giữ trước và sau khi nhường quyền chạy; mỗi tác vụ có ngăn xếp máy riêng.
        int giáTrịCụcBộ = sốHiệu * 100;
        for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < 10; chỉSốVòngLặp++) {
            if (thứTựTácVụ % 2 + 1 != sốHiệu) lỗiTácVụ++;
            thứTựTácVụ++;
            giáTrịCụcBộ += chỉSốVòngLặp + sốHiệu;
            tổngTácVụ[sốHiệu] = giáTrịCụcBộ;
            cácLầnLặpTácVụ[sốHiệu]++;
            BoMạch.nhườngBộXửLýTrungTâm();
            if (giáTrịCụcBộ != tổngTácVụ[sốHiệu]) lỗiTácVụ++;
        }
    }
    static void thửCácTácVụ() {
        thứTựTácVụ = 0; lỗiTácVụ = 0;
        cácLầnLặpTácVụ[1] = 0; cácLầnLặpTácVụ[2] = 0;
        xácMinh(BoMạch.tạoTácVụ(1) == 0 && BoMạch.tạoTácVụ(2) == 0, 20);
        int sốLượngPhépXoay = 0;
        while (BoMạch.trạngTháiTácVụ(1) != 0 || BoMạch.trạngTháiTácVụ(2) != 0) {
            BoMạch.nhườngBộXửLýTrungTâm();
            xácMinh(++sốLượngPhépXoay < 100, 21);
        }
        xácMinh(cácLầnLặpTácVụ[1] == 10 && cácLầnLặpTácVụ[2] == 10 && thứTựTácVụ == 20 && lỗiTácVụ == 0, 22);
        xácMinh(tổngTácVụ[1] == 155 && tổngTácVụ[2] == 265, 23);
        VàoRaThiếtBịCuối.ghi("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void hìnhChữNhật(int vịTríNgang, int vịTríDọc, int giáTrịRộng, int giáTrịCao, int giáTrịMàu) {
        for (int tọaĐộY = vịTríDọc; tọaĐộY < vịTríDọc + giáTrịCao; tọaĐộY++)
            for (int tọaĐộX = vịTríNgang; tọaĐộX < vịTríNgang + giáTrịRộng; tọaĐộX++) BoMạch.đặtĐiểmẢnhMànHình(tọaĐộX, tọaĐộY, giáTrịMàu);
    }
    static void MànHình() {
        if (BoMạch.chuẩnBịMànHình() == 0) { VàoRaThiếtBịCuối.ghi("FRAMEBUFFER unavailable\n"); return; }
        hìnhChữNhật(0, 0, BoMạch.rộngMànHình(), BoMạch.caoMànHình(), 0x302018);
        hìnhChữNhật(40, 40, 560, 400, 0xefe8e2);
        hìnhChữNhật(40, 40, 560, 40, 0x905020);
        hìnhChữNhật(60, 110, 240, 140, 0x90b050);
        hìnhChữNhật(320, 110, 260, 140, 0xd0a040);
        hìnhChữNhật(60, 290, 520, 120, 0xd8d0c8);
        VàoRaThiếtBịCuối.ghi("FRAMEBUFFER PASS "); VàoRaThiếtBịCuối.trịSố(BoMạch.rộngMànHình()); VàoRaThiếtBịCuối.KýTự('x');
        VàoRaThiếtBịCuối.trịSố(BoMạch.caoMànHình()); VàoRaThiếtBịCuối.ghi(" RGB32 (drawing only)\n");
    }
    static void thửC() {
        int kếtQuả = BoMạch.thửCộngCộng();
        xácMinh(kếtQuả == 0, 100 + kếtQuả);
        VàoRaThiếtBịCuối.ghi("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void thửCácChươngTrìnhNgườiDùng() {
        xácMinh(BoMạch.kiểmTraChươngTrìnhNgườiDùng() == 0, 200);
        VàoRaThiếtBịCuối.ghi("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int kếtQuảBanĐầu = BoMạch.chạyChươngTrìnhNgườiDùng(0);
        if (kếtQuảBanĐầu != 0) { VàoRaThiếtBịCuối.ghi("USER DEMO RESULT "); VàoRaThiếtBịCuối.trịSố(kếtQuảBanĐầu); VàoRaThiếtBịCuối.KýTự(10); }
        xácMinh(kếtQuảBanĐầu == 0, 201);
        VàoRaThiếtBịCuối.ghi("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] cácGiáTrịDựKiến = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int sốHiệu = 0; sốHiệu < cácGiáTrịDựKiến.length; sốHiệu++) {
            VàoRaThiếtBịCuối.ghi("USER CHECK "); VàoRaThiếtBịCuối.trịSố(sốHiệu); VàoRaThiếtBịCuối.KýTự(10);
            int kếtQuả = BoMạch.chạyChươngTrìnhNgườiDùng(sốHiệu + 1);
            if (kếtQuả != cácGiáTrịDựKiến[sốHiệu]) { VàoRaThiếtBịCuối.ghi("USER RESULT "); VàoRaThiếtBịCuối.trịSố(kếtQuả); VàoRaThiếtBịCuối.KýTự(10); }
            xácMinh(kếtQuả == cácGiáTrịDựKiến[sốHiệu], 210 + sốHiệu);
        }
        xácMinh(BoMạch.chạyChươngTrìnhNgườiDùng(0) == 0, 220);
        VàoRaThiếtBịCuối.ghi("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void thửKếtNốiMạng() {
        int kếtQuả = BoMạch.chạyChươngTrìnhNgườiDùng(9);
        if (kếtQuả != 0) { VàoRaThiếtBịCuối.ghi("UDP RESULT "); VàoRaThiếtBịCuối.trịSố(kếtQuả); VàoRaThiếtBịCuối.KýTự(10); }
        xácMinh(kếtQuả == 0, 230);
    }
    static void thôngTinHệThống() {
        VàoRaThiếtBịCuối.ghi("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        VàoRaThiếtBịCuối.ghi("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        VàoRaThiếtBịCuối.ghi("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        VàoRaThiếtBịCuối.ghi("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        VàoRaThiếtBịCuối.ghi("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void chạy() {
        VàoRaThiếtBịCuối.ghi("WorldOS vi · Xin chào · 😀\n");
        thửSốHọc();
        thửC();
        thửCácTácVụ();
        MànHình();
        thửCácChươngTrìnhNgườiDùng();
        thửKếtNốiMạng();
        VàoRaThiếtBịCuối.ghi("NATIVE READY\n");
        TrìnhThôngDịchLệnh.thựcThiLệnh();
    }
}
