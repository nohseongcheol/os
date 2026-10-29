// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Đầu ra nối tiếp COM1 và màn hình chữ VGA 80x25. Văn bản Unicode được gửi tới thiết bị cuối nối tiếp bằng UTF-8. */
public final class ĐầuCuốiVănBản {
    static int mụcÔ = 0;
    static int giáTrịMàu = 7;

    static void chuẩnBị() {
        ThiếtBị.ghiByteVàoRa(0x3f9, 0);
        ThiếtBị.ghiByteVàoRa(0x3fb, 0x80);
        ThiếtBị.ghiByteVàoRa(0x3f8, 1);
        ThiếtBị.ghiByteVàoRa(0x3f9, 0);
        ThiếtBị.ghiByteVàoRa(0x3fb, 3);
        ThiếtBị.ghiByteVàoRa(0x3fa, 0xc7);
        ThiếtBị.ghiByteVàoRa(0x3fc, 0x0b);
        xóaMục();
    }

    static void byteNốiTiếp(int giáTrị) {
        int sốLượngSựLặp = 100000;
        while ((ThiếtBị.đọcByteVàoRa(0x3fd) & 0x20) == 0 && sốLượngSựLặp > 0) sốLượngSựLặp--;
        if (sốLượngSựLặp > 0) ThiếtBị.ghiByteVàoRa(0x3f8, giáTrị);
    }

    static void xóaMục() {
        for (int sốHiệu = 0; sốHiệu < 2000; sốHiệu++) {
            ThiếtBị.ghiBộNhớ(0xb8000 + sốHiệu * 2, 32);
            ThiếtBị.ghiBộNhớ(0xb8001 + sốHiệu * 2, giáTrịMàu);
        }
        mụcÔ = 0;
        giáTrịConTrỏVănBản();
    }

    static void giáTrịConTrỏVănBản() {
        ThiếtBị.ghiByteVàoRa(0x3d4, 14);
        ThiếtBị.ghiByteVàoRa(0x3d5, mụcÔ >> 8);
        ThiếtBị.ghiByteVàoRa(0x3d4, 15);
        ThiếtBị.ghiByteVàoRa(0x3d5, mụcÔ & 255);
    }

    static void kýTựMànHình(int giáTrị) {
        if (giáTrị == 13) return;
        if (giáTrị == 10) {
            mụcÔ = (mụcÔ / 80 + 1) * 80;
        } else if (giáTrị == 8) {
            if (mụcÔ > 0) {
                mụcÔ--;
                ThiếtBị.ghiBộNhớ(0xb8000 + mụcÔ * 2, 32);
            }
        } else {
            ThiếtBị.ghiBộNhớ(0xb8000 + mụcÔ * 2, giáTrị < 128 ? giáTrị : '?');
            ThiếtBị.ghiBộNhớ(0xb8001 + mụcÔ * 2, giáTrịMàu);
            mụcÔ++;
        }
        if (mụcÔ >= 2000) {
            for (int sốHiệu = 0; sốHiệu < 3840; sốHiệu++)
                ThiếtBị.ghiBộNhớ(0xb8000 + sốHiệu, ThiếtBị.đọcBộNhớ(0xb80a0 + sốHiệu));
            for (int sốHiệu = 1920; sốHiệu < 2000; sốHiệu++) {
                ThiếtBị.ghiBộNhớ(0xb8000 + sốHiệu * 2, 32);
                ThiếtBị.ghiBộNhớ(0xb8001 + sốHiệu * 2, giáTrịMàu);
            }
            mụcÔ = 1920;
        }
        giáTrịConTrỏVănBản();
    }

    static void KýTự(int giáTrị) {
        if (giáTrị < 128) {
            if (giáTrị == 10) byteNốiTiếp(13);
            byteNốiTiếp(giáTrị);
        } else if (giáTrị < 2048) {
            byteNốiTiếp(0xc0 | (giáTrị >> 6));
            byteNốiTiếp(0x80 | (giáTrị & 63));
        } else {
            byteNốiTiếp(0xe0 | (giáTrị >> 12));
            byteNốiTiếp(0x80 | ((giáTrị >> 6) & 63));
            byteNốiTiếp(0x80 | (giáTrị & 63));
        }
        kýTựMànHình(giáTrị);
    }

    static void ghi(String giáTrịNộiDung) {
        for (int sốHiệu = 0; sốHiệu < giáTrịNộiDung.length(); sốHiệu++) KýTự(giáTrịNộiDung.charAt(sốHiệu));
    }

    static void ghiSố(int giáTrị) {
        // Không đổi sang số dương nên cả Integer.MIN_VALUE cũng an toàn.
        if (giáTrị < 0) KýTự('-');
        else giáTrị = -giáTrị;
        int chỉSốVịTrí = 1000000000;
        boolean chạy = false;
        while (chỉSốVịTrí > 0) {
            int giáTrịChữSố = -(giáTrị / chỉSốVịTrí);
            if (giáTrịChữSố != 0 || chạy || chỉSốVịTrí == 1) {
                KýTự('0' + giáTrịChữSố);
                chạy = true;
            }
            giáTrị %= chỉSốVịTrí;
            chỉSốVịTrí /= 10;
        }
    }

    static int đọcNốiTiếp() {
        if ((ThiếtBị.đọcByteVàoRa(0x3fd) & 1) != 0) return ThiếtBị.đọcByteVàoRa(0x3f8);
        return -1;
    }
}
