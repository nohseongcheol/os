// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Màn hình khởi chạy nhỏ trên bộ đệm khung hình, điều khiển bằng TAB/ENTER/Q qua UART. Giao diện giới hạn dùng phông chữ Latinh 5x7 tự định nghĩa; không có Swing, USB HID hay bộ gõ đầy đủ. */
public final class MànLàmViệc {
    static String cácGiáTrịKýTự = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-.:";
    // Mỗi ký tự có 7 hàng, mỗi hàng biểu diễn bằng hai chữ số thập lục phân. Phông chữ 5x7 do dự án tự định nghĩa.
    static String danhSáchCácHình =
        "0E11111F111111" + "1E11111E11111E" + "0F10101010100F" + "1E11111111111E" +
        "1F10101E10101F" + "1F10101E101010" + "0F10101711110F" + "1111111F111111" +
        "0E04040404040E" + "0702020212120C" + "11121418141211" + "1010101010101F" +
        "111B1515111111" + "11191915131311" + "0E11111111110E" + "1E11111E101010" +
        "0E11111115120D" + "1E11111E141211" + "0F10100E01011E" + "1F040404040404" +
        "1111111111110E" + "11111111110A04" + "11111115151B11" + "11110A040A1111" +
        "11110A04040404" + "1F01020408101F" + "0E11131519110E" + "040C040404040E" +
        "0E11010204081F" + "1E01010601011E" + "02060A121F0202" + "1F10101E01011E" +
        "0E10101E11110E" + "1F010204080808" + "0E11110E11110E" + "0E11110F01010E" +
        "0004041F040400" + "0000001F000000" + "00000000000C0C" + "000C0C000C0C00";
    static int giáTrịChữSố(int giáTrịKýTự) { return giáTrịKýTự <= '9' ? giáTrịKýTự - '0' : giáTrịKýTự - 'A' + 10; }
    static void vănBản(int vịTríNgang, int vịTríDọc, String giáTrịNộiDung, int giáTrịMàu) {
        for (int giáTrịKýTự = 0; giáTrịKýTự < giáTrịNộiDung.length(); giáTrịKýTự++) {
            int giáTrịĐãTìmThấy = -1;
            for (int ứngViên = 0; ứngViên < cácGiáTrịKýTự.length(); ứngViên++) if (cácGiáTrịKýTự.charAt(ứngViên) == giáTrịNộiDung.charAt(giáTrịKýTự)) giáTrịĐãTìmThấy = ứngViên;
            if (giáTrịĐãTìmThấy < 0) continue;
            for (int giáTrịHàng = 0; giáTrịHàng < 7; giáTrịHàng++) {
                int vịTrí = giáTrịĐãTìmThấy * 14 + giáTrịHàng * 2;
                int giáTrịBit = giáTrịChữSố(danhSáchCácHình.charAt(vịTrí)) * 16 + giáTrịChữSố(danhSáchCácHình.charAt(vịTrí + 1));
                for (int giáTrịCột = 0; giáTrịCột < 5; giáTrịCột++) if ((giáTrịBit & (16 >> giáTrịCột)) != 0)
                    Nhân.hìnhChữNhật(vịTríNgang + giáTrịKýTự * 12 + giáTrịCột * 2, vịTríDọc + giáTrịHàng * 2, 2, 2, giáTrịMàu);
            }
        }
    }
    static void mànHìnhTô(int giáTrịViệcChọn, String giáTrịTrạngThái) {
        Nhân.hìnhChữNhật(0, 0, BoMạch.rộngMànHình(), BoMạch.caoMànHình(), 0x302018);
        Nhân.hìnhChữNhật(32, 24, 576, 432, 0xefe8e2);
        Nhân.hìnhChữNhật(32, 24, 576, 48, 0x905020);
        vănBản(52, 40, "JKOROS PROGRAMS", 0xffffff);
        for (int sốHiệu = 0; sốHiệu < 5; sốHiệu++) {
            Nhân.hìnhChữNhật(64, 112 + sốHiệu * 52, 512, 40, sốHiệu == giáTrịViệcChọn ? 0xd0a040 : 0xd8d0c8);
            vănBản(84, 128 + sốHiệu * 52, sốHiệu == 0 ? "RUN C++ FILE PROGRAM" : sốHiệu == 1 ? "RUN UDP LOOPBACK" : sốHiệu == 2 ? "COMPILE AND RUN JAVA" : sốHiệu == 3 ? "RUN MICROPYTHON" : "OPEN TERMINAL", 0x201810);
        }
        vănBản(68, 384, giáTrịTrạngThái, 0x205020);
        vănBản(52, 420, "TAB SELECT  ENTER RUN  Q EXIT", 0x302018);
    }
    public static void thựcThiLệnh() {
        if (BoMạch.chuẩnBịMànHình() == 0) { VàoRaThiếtBịCuối.ghi("GUI unavailable\n"); return; }
        int giáTrịViệcChọn = 0;
        String giáTrịTrạngThái = "READY";
        boolean dòngTrướcĐó = TrìnhThôngDịchLệnh.dòngTrướcĐó;
        mànHìnhTô(giáTrịViệcChọn, giáTrịTrạngThái);
        VàoRaThiếtBịCuối.ghi("GUI READY: UART TAB selects, ENTER runs, Q exits\n");
        while (true) {
            int giáTrịVào = BoMạch.đọcNốiTiếp();
            if (giáTrịVào < 0) { BoMạch.nhườngBộXửLýTrungTâm(); continue; }
            if (giáTrịVào == 10 && dòngTrướcĐó) { dòngTrướcĐó = false; continue; }
            dòngTrướcĐó = giáTrịVào == 13;
            if (giáTrịVào >= '1' && giáTrịVào <= '5') { giáTrịViệcChọn = giáTrịVào - '1'; giáTrịVào = 13; }
            if (giáTrịVào == 't' || giáTrịVào == 'T') { TrìnhThôngDịchLệnh.thiếtBịCuối(false); return; }
            if (giáTrịVào == 'q' || giáTrịVào == 'Q' || giáTrịVào == 27) break;
            if (giáTrịVào == 9 || giáTrịVào == 'j') {
                giáTrịViệcChọn = (giáTrịViệcChọn + 1) % 5; mànHìnhTô(giáTrịViệcChọn, giáTrịTrạngThái); VàoRaThiếtBịCuối.ghi("GUI FOCUS "); VàoRaThiếtBịCuối.trịSố(giáTrịViệcChọn); VàoRaThiếtBịCuối.KýTự(10);
            } else if (giáTrịVào == 13 || giáTrịVào == 10) {
                if (giáTrịViệcChọn == 4) { TrìnhThôngDịchLệnh.thiếtBịCuối(false); return; }
                int kếtQuả;
                if (giáTrịViệcChọn < 2) kếtQuả = BoMạch.chạyChươngTrìnhNgườiDùng(giáTrịViệcChọn == 0 ? 0 : 9);
                else if (giáTrịViệcChọn == 2) {
                    kếtQuả = TrìnhThôngDịchLệnh.chạyVíDụ(10, "Hello.java");
                    if (kếtQuả == 0) kếtQuả = TrìnhThôngDịchLệnh.chạyVíDụ(11, "Hello");
                } else kếtQuả = TrìnhThôngDịchLệnh.chạyVíDụ(12, "hello.py");
                giáTrịTrạngThái = kếtQuả != 0 ? "PROGRAM FAILED" : giáTrịViệcChọn == 0 ? "C++ FILE OK" : giáTrịViệcChọn == 1 ? "UDP LOOPBACK OK" : giáTrịViệcChọn == 2 ? "JAVA OK" : "MICROPYTHON OK";
                mànHìnhTô(giáTrịViệcChọn, giáTrịTrạngThái);
                VàoRaThiếtBịCuối.ghi("GUI ACTION "); VàoRaThiếtBịCuối.trịSố(giáTrịViệcChọn); VàoRaThiếtBịCuối.ghi(" RESULT "); VàoRaThiếtBịCuối.trịSố(kếtQuả); VàoRaThiếtBịCuối.KýTự(10);
            }
        }
        Nhân.MànHình();
        VàoRaThiếtBịCuối.ghi("GUI EXIT\n");
    }
}
