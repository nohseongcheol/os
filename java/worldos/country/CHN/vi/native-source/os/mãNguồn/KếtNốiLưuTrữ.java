// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Các cung logic 512 byte của thiết bị IDE đầu tiên. Lớp này không định dạng hay xóa thiết bị tùy ý. */
public final class KếtNốiLưuTrữ {
    static boolean làSẵnCó = false;
    static int[] dữLiệuMụcĐoạn = new int[512];
    static void chờNgắn() {
        for (int sốHiệu = 0; sốHiệu < 4; sốHiệu++) ThiếtBị.đọcByteVàoRa(0x3f6);
    }
    static int chờSẵnSàngĐếnKhi(boolean bắtBuộcDữLiệu) {
        int chạy = ThiếtBị.miliGiây();
        while (ThiếtBị.miliGiây() - chạy < 500) {
            int giáTrịTrạngThái = ThiếtBị.đọcByteVàoRa(0x1f7);
            if (giáTrịTrạngThái == 0 || giáTrịTrạngThái == 255) return -19;
            if ((giáTrịTrạngThái & 128) == 0) {
                if ((giáTrịTrạngThái & 33) != 0) return -5;
                if (!bắtBuộcDữLiệu || (giáTrịTrạngThái & 8) != 0) return 0;
            }
            ThiếtBị.nhườngNgắn();
        }
        return -110;
    }
    static int yêuCầu(int giáTrịMụcĐoạn, int lệnh) {
        if (giáTrịMụcĐoạn < 0 || giáTrịMụcĐoạn >= 2048) return -22;
        ThiếtBị.ghiByteVàoRa(0x3f6, 2); // Thăm dò; không dùng IDE IRQ.
        ThiếtBị.ghiByteVàoRa(0x1f6, 0xe0); chờNgắn();
        int kếtQuả = chờSẵnSàngĐếnKhi(false);
        if (kếtQuả < 0) return kếtQuả;
        ThiếtBị.ghiByteVàoRa(0x1f2, 1);
        ThiếtBị.ghiByteVàoRa(0x1f3, giáTrịMụcĐoạn & 255);
        ThiếtBị.ghiByteVàoRa(0x1f4, (giáTrịMụcĐoạn >>> 8) & 255);
        ThiếtBị.ghiByteVàoRa(0x1f5, 0);
        ThiếtBị.ghiByteVàoRa(0x1f7, lệnh); chờNgắn();
        return chờSẵnSàngĐếnKhi(true);
    }
    static int đọc(int giáTrịMụcĐoạn) {
        int kếtQuả = yêuCầu(giáTrịMụcĐoạn, 0x20);
        if (kếtQuả < 0) return kếtQuả;
        for (int sốHiệu = 0; sốHiệu < 256; sốHiệu++) {
            int giáTrị = ThiếtBị.đọcNgắnKiểuVàoRa(0x1f0);
            dữLiệuMụcĐoạn[sốHiệu * 2] = giáTrị & 255; dữLiệuMụcĐoạn[sốHiệu * 2 + 1] = giáTrị >>> 8;
        }
        chờNgắn(); return chờSẵnSàngĐếnKhi(false);
    }
    static int ghi(int giáTrịMụcĐoạn) {
        if (!làSẵnCó || giáTrịMụcĐoạn < 1 || giáTrịMụcĐoạn > 518) return -19;
        int kếtQuả = yêuCầu(giáTrịMụcĐoạn, 0x30);
        if (kếtQuả < 0) return kếtQuả;
        for (int sốHiệu = 0; sốHiệu < 256; sốHiệu++)
            ThiếtBị.ghiNgắnKiểuVàoRa(0x1f0, dữLiệuMụcĐoạn[sốHiệu * 2] | dữLiệuMụcĐoạn[sốHiệu * 2 + 1] << 8);
        chờNgắn(); return chờSẵnSàngĐếnKhi(false);
    }
    static int đầuRaĐẩyĐệm() {
        if (!làSẵnCó) return -19;
        ThiếtBị.ghiByteVàoRa(0x1f7, 0xe7); chờNgắn();
        return chờSẵnSàngĐếnKhi(false);
    }
    static int phânTíchCúPhápSốNguyên(int vịTrí) {
        return dữLiệuMụcĐoạn[vịTrí] | dữLiệuMụcĐoạn[vịTrí + 1] << 8 | dữLiệuMụcĐoạn[vịTrí + 2] << 16 | dữLiệuMụcĐoạn[vịTrí + 3] << 24;
    }
    static void ghiGiáTrịSốNguyên(int vịTrí, int giáTrị) {
        for (int sốHiệu = 0; sốHiệu < 4; sốHiệu++) dữLiệuMụcĐoạn[vịTrí + sốHiệu] = (giáTrị >>> (sốHiệu * 8)) & 255;
    }
}
