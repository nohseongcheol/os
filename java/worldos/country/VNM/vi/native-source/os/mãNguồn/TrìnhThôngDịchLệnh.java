// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Trình thông dịch lệnh nối tiếp/PS2 nhỏ, không ghi đĩa. */
public final class TrìnhThôngDịchLệnh {
    static int[] giáTrịVào = new int[128];
    static int độDài = 0;
    static boolean dòngTrướcĐóĐếnTrảVề = false;
    static boolean trànDòng = false;

    static boolean lệnh(String tên) {
        if (độDài < tên.length()) return false;
        for (int sốHiệu = 0; sốHiệu < tên.length(); sốHiệu++)
            if (giáTrịVào[sốHiệu] != tên.charAt(sốHiệu)) return false;
        return độDài == tên.length() || giáTrịVào[tên.length()] == ' ';
    }

    static void hiệnTrợGiúp() {
        ĐầuCuốiVănBản.ghi("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        ĐầuCuốiVănBản.ghi("apps | run NAME [ARGS] | net\n");
        ĐầuCuốiVănBản.ghi("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        ĐầuCuốiVănBản.ghi("sync (연결된 JKSTORE1 giáTrịCất 장치에 Tệp 보존)\n");
    }

    static void mụcGiáTrịTiếnTrình() {
        if (độDài == 0) return;
        if (lệnh("help")) hiệnTrợGiúp();
        else if (lệnh("sync")) {
            int kếtQuả = LưuGiữTệp.đồngBộHóa();
            ĐầuCuốiVănBản.ghi("Sync: "); ĐầuCuốiVănBản.ghiSố(kếtQuả); ĐầuCuốiVănBản.KýTự(10);
        }
        else if (lệnh("ls")) HệTệpBộNhớ.danhSáchMục();
        else if (lệnh("edit")) HệTệpBộNhớ.lệnh(giáTrịVào, 4, độDài, 0);
        else if (lệnh("cat")) HệTệpBộNhớ.lệnh(giáTrịVào, 3, độDài, 1);
        else if (lệnh("rm")) HệTệpBộNhớ.lệnh(giáTrịVào, 2, độDài, 2);
        else if (lệnh("java") || lệnh("javac")) {
            int kếtQuả = QuảnLýThựcThi.thựcThiLệnh(giáTrịVào, 0, độDài);
            ĐầuCuốiVănBản.ghi("Exit: "); ĐầuCuốiVănBản.ghiSố(kếtQuả); ĐầuCuốiVănBản.KýTự(10);
        }
        else if (lệnh("apps")) QuảnLýThựcThi.danhSáchMục();
        else if (lệnh("net")) NgănXếpMạng.giáTrịTrạngThái();
        else if (lệnh("run")) {
            int kếtQuả = QuảnLýThựcThi.thựcThiLệnh(giáTrịVào, 3, độDài);
            ĐầuCuốiVănBản.ghi("Exit: "); ĐầuCuốiVănBản.ghiSố(kếtQuả); ĐầuCuốiVănBản.ghi("\n");
        } else if (lệnh("info")) {
            ĐầuCuốiVănBản.ghi("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (lệnh("mem")) {
            ĐầuCuốiVănBản.ghi("bênThượng BộNhớ miềnĐịaChỉ(KiB): "); ĐầuCuốiVănBản.ghiSố(VùngNhớ.cỡBộNhớThượng());
            ĐầuCuốiVănBản.ghi("\n배열 동적 BộNhớ miềnĐịaChỉ(giáTrịByte): "); ĐầuCuốiVănBản.ghiSố(ThiếtBị.cáchDùngMảng());
            ĐầuCuốiVănBản.ghi(" / 262144\n작업 miềnĐịaChỉ giáTrịMụcĐoạn: "); ĐầuCuốiVănBản.ghiSố(VùngNhớ.sốLượngMụcĐãDùng());
            ĐầuCuốiVănBản.ghi(" / 8 (각 4096바이트)\n");
        } else if (lệnh("alloc")) {
            int sốHiệu = VùngNhớ.cấpPhátLưuTrữ();
            ĐầuCuốiVănBản.ghi("giáTrịMụcĐoạn sốHiệu: "); ĐầuCuốiVănBản.ghiSố(sốHiệu); ĐầuCuốiVănBản.ghi("\n");
        } else if (lệnh("free")) {
            if (độDài == 6 && giáTrịVào[4] == ' ' && giáTrịVào[5] >= '0' && giáTrịVào[5] <= '7') {
                ĐầuCuốiVănBản.ghi(VùngNhớ.kếtQuảTrảVề(giáTrịVào[5] - '0') ? "반환됨\n" : "할당되지 않은 giáTrịMụcĐoạn\n");
            } else ĐầuCuốiVănBản.ghi("사용법: free 0..7\n");
        } else if (lệnh("echo")) {
            for (int sốHiệu = 5; sốHiệu < độDài; sốHiệu++) ĐầuCuốiVănBản.KýTự(giáTrịVào[sốHiệu]);
            ĐầuCuốiVănBản.KýTự(10);
        } else if (lệnh("clear")) ĐầuCuốiVănBản.xóaMục();
        else if (lệnh("test")) Nhân.KiểmThử();
        else if (lệnh("halt")) {
            ĐầuCuốiVănBản.ghi("HALTED\n");
            ThiếtBị.việcThựcThiDừngHẳn();
        } else ĐầuCuốiVănBản.ghi("알 trịSố 없는 명령입니다. help를 입력하세요.\n");
    }

    static void chấpNhậnGhiVà(int giáTrị) {
        if (giáTrị == 10 && dòngTrướcĐóĐếnTrảVề) { dòngTrướcĐóĐếnTrảVề = false; return; }
        dòngTrướcĐóĐếnTrảVề = giáTrị == 13;
        if (giáTrị == 10 || giáTrị == 13) {
            ĐầuCuốiVănBản.KýTự(10);
            if (HệTệpBộNhớ.làĐangSửa) HệTệpBộNhớ.dòngĐãSửa(giáTrịVào, độDài, trànDòng);
            else mụcGiáTrịTiếnTrình();
            độDài = 0;
            trànDòng = false;
            ĐầuCuốiVănBản.ghi(HệTệpBộNhớ.làĐangSửa ? "...> " : "jkoros> ");
        } else if (giáTrị == 8 || giáTrị == 127) {
            if (độDài > 0) {
                độDài--;
                ĐầuCuốiVănBản.byteNốiTiếp(8); ĐầuCuốiVănBản.byteNốiTiếp(32); ĐầuCuốiVănBản.byteNốiTiếp(8);
                ĐầuCuốiVănBản.kýTựMànHình(8);
            }
        } else if (giáTrị >= 32 && giáTrị < 127 && độDài < giáTrịVào.length) {
            giáTrịVào[độDài++] = giáTrị;
            ĐầuCuốiVănBản.KýTự(giáTrị);
        } else if (giáTrị >= 32 && giáTrị < 127) trànDòng = true;
    }

    static void chạy() {
        hiệnTrợGiúp();
        ĐầuCuốiVănBản.ghi("READY\njkoros> ");
        while (true) {
            int giáTrị = ĐầuCuốiVănBản.đọcNốiTiếp();
            if (giáTrị < 0) giáTrị = BànPhím.đọc();
            if (giáTrị >= 0) chấpNhậnGhiVà(giáTrị);
            else { NgănXếpMạng.xácMinh(); ThiếtBị.nhườngNgắn(); }
        }
    }
}
