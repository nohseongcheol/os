// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), một bộ đệm gửi và vòng đệm nhận 8 KiB. Dùng thăm dò thay cho ngắt. */
public final class TrìnhĐiềuKhiểnMạng {
    static int địaChỉCơSởVàoRa = 0;
    static int nhậnVịTrí = 0, ôTruyền = 0;
    static int[] địaChỉThiếtBị = new int[6];
    static int sốLượngTruyền = 0, nhậnSốLượng = 0, sốLượngLỗi = 0;

    static int đọcCácThiếtLập(int sốThiếtBị, int vịTrí) {
        ThiếtBị.ghiSốNguyênVàoRa(0xcf8, 0x80000000 | (sốThiếtBị << 11) | vịTrí);
        return ThiếtBị.đọcSốNguyênVàoRa(0xcfc);
    }

    static boolean chuẩnBị() {
        int sốThiếtBị = -1;
        for (int sốHiệu = 0; sốHiệu < 32; sốHiệu++) {
            if (đọcCácThiếtLập(sốHiệu, 0) == 0x813910ec) { sốThiếtBị = sốHiệu; break; }
        }
        if (sốThiếtBị < 0) return false;
        int giáTrịMặcĐịnh = đọcCácThiếtLập(sốThiếtBị, 0x10);
        if ((giáTrịMặcĐịnh & 1) == 0 || (giáTrịMặcĐịnh & 0xfffffffc) < 0x100 || (giáTrịMặcĐịnh & 0xfffffffc) > 65535) return false;
        địaChỉCơSởVàoRa = giáTrịMặcĐịnh & 0xfffc;
        int lệnh = đọcCácThiếtLập(sốThiếtBị, 4);
        ThiếtBị.ghiSốNguyênVàoRa(0xcf8, 0x80000004 | (sốThiếtBị << 11));
        ThiếtBị.ghiNgắnKiểuVàoRa(0xcfc, lệnh | 5); // Bật I/O và quyền làm chủ bus; không đổi các bit trạng thái PCI.
        ThiếtBị.ghiByteVàoRa(địaChỉCơSởVàoRa + 0x52, 0);
        if (!đặtLạiGiáTrị()) { địaChỉCơSởVàoRa = 0; return false; }
        for (int sốHiệu = 0; sốHiệu < 6; sốHiệu++) địaChỉThiếtBị[sốHiệu] = ThiếtBị.đọcByteVàoRa(địaChỉCơSởVàoRa + sốHiệu);
        return true;
    }

    static boolean đặtLạiGiáTrị() {
        ThiếtBị.ghiByteVàoRa(địaChỉCơSởVàoRa + 0x37, 0x10);
        int chạy = ThiếtBị.miliGiây();
        while ((ThiếtBị.đọcByteVàoRa(địaChỉCơSởVàoRa + 0x37) & 0x10) != 0)
            if (ThiếtBị.miliGiây() - chạy > 100) return false;
        nhậnVịTrí = 0; ôTruyền = 0;
        ThiếtBị.ghiSốNguyênVàoRa(địaChỉCơSởVàoRa + 0x30, ThiếtBị.bộNhớMạng());
        for (int sốHiệu = 0; sốHiệu < 4; sốHiệu++) ThiếtBị.ghiSốNguyênVàoRa(địaChỉCơSởVàoRa + 0x20 + sốHiệu * 4, ThiếtBị.bộNhớMạng() + 12288);
        ThiếtBị.ghiNgắnKiểuVàoRa(địaChỉCơSởVàoRa + 0x3c, 0);
        ThiếtBị.ghiNgắnKiểuVàoRa(địaChỉCơSởVàoRa + 0x3e, 0xffff);
        ThiếtBị.ghiByteVàoRa(địaChỉCơSởVàoRa + 0x37, 0x0c);
        ThiếtBị.ghiSốNguyênVàoRa(địaChỉCơSởVàoRa + 0x44, 0x0000e78a); // Nhận địa chỉ bản thân và quảng bá; lưu liên tục khi vòng lại, 8 KiB.
        ThiếtBị.ghiSốNguyênVàoRa(địaChỉCơSởVàoRa + 0x40, 0x03000600);
        return true;
    }

    static int gửi(int[] DữLiệu, int độDài) {
        if (địaChỉCơSởVàoRa == 0) return -19;
        if (độDài < 14 || độDài > 1514) return -90;
        int cổngTìnhTrạng = địaChỉCơSởVàoRa + 0x10 + ôTruyền * 4;
        int chạy = ThiếtBị.miliGiây();
        while ((ThiếtBị.đọcSốNguyênVàoRa(cổngTìnhTrạng) & 0x2000) == 0)
            if (ThiếtBị.miliGiây() - chạy > 100) return -110;
        int cỡ = độDài < 60 ? 60 : độDài;
        for (int sốHiệu = 0; sốHiệu < cỡ; sốHiệu++)
            ThiếtBị.ghiBộNhớ(ThiếtBị.bộNhớMạng() + 12288 + sốHiệu, sốHiệu < độDài ? DữLiệu[sốHiệu] : 0);
        ThiếtBị.ghiSốNguyênVàoRa(cổngTìnhTrạng, cỡ | 0x00080000);
        chạy = ThiếtBị.miliGiây();
        while ((ThiếtBị.đọcSốNguyênVàoRa(cổngTìnhTrạng) & 0xe0008000) == 0)
            if (ThiếtBị.miliGiây() - chạy > 100) return -110;
        if ((ThiếtBị.đọcSốNguyênVàoRa(cổngTìnhTrạng) & 0x8000) == 0) { sốLượngLỗi++; return -5; }
        ôTruyền = (ôTruyền + 1) & 3;
        sốLượngTruyền++;
        return độDài;
    }

    static int nhận(int[] DữLiệu) {
        if (địaChỉCơSởVàoRa == 0) return 0;
        if ((ThiếtBị.đọcByteVàoRa(địaChỉCơSởVàoRa + 0x3e) & 0x50) != 0) {
            sốLượngLỗi++;
            if (!đặtLạiGiáTrị()) địaChỉCơSởVàoRa = 0;
            return 0;
        }
        if ((ThiếtBị.đọcByteVàoRa(địaChỉCơSởVàoRa + 0x37) & 1) != 0) return 0;
        int giáTrịĐầu = ThiếtBị.bộNhớMạng() + nhậnVịTrí;
        int giáTrịTrạngThái = QuảnLýThựcThi.giáTrịNgắnKiểu(giáTrịĐầu), cỡ = QuảnLýThựcThi.giáTrịNgắnKiểu(giáTrịĐầu + 2);
        if (cỡ == 0xfff0) return 0; // DMA đang tiến hành.
        if (cỡ < 4 || cỡ > 1518) {
            sốLượngLỗi++;
            if (!đặtLạiGiáTrị()) địaChỉCơSởVàoRa = 0;
            return 0;
        }
        int độDài = cỡ - 4;
        if ((giáTrịTrạngThái & 1) != 0) {
            for (int sốHiệu = 0; sốHiệu < độDài; sốHiệu++) DữLiệu[sốHiệu] = ThiếtBị.đọcBộNhớ(giáTrịĐầu + 4 + sốHiệu);
            nhậnSốLượng++;
        } else { độDài = 0; sốLượngLỗi++; }
        nhậnVịTrí = (nhậnVịTrí + cỡ + 4 + 3) & ~3;
        nhậnVịTrí &= 8191;
        ThiếtBị.ghiNgắnKiểuVàoRa(địaChỉCơSởVàoRa + 0x38, (nhậnVịTrí - 16) & 65535);
        ThiếtBị.ghiNgắnKiểuVàoRa(địaChỉCơSởVàoRa + 0x3e, 0x000f);
        return độDài;
    }
}
