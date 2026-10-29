// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** COM1 직렬 출력과 VGA 80x25 문자 화면. 한글은 직렬 단말에 UTF-8로 출력한다. */
public final class TEXT_Tauranga {
    static int kāniwha_tāurunga = 0;
    static int 색 = 7;

    static void Whakarite() {
        pūkoro_uara.입출력바이트쓰기(0x3f9, 0);
        pūkoro_uara.입출력바이트쓰기(0x3fb, 0x80);
        pūkoro_uara.입출력바이트쓰기(0x3f8, 1);
        pūkoro_uara.입출력바이트쓰기(0x3f9, 0);
        pūkoro_uara.입출력바이트쓰기(0x3fb, 3);
        pūkoro_uara.입출력바이트쓰기(0x3fa, 0xc7);
        pūkoro_uara.입출력바이트쓰기(0x3fc, 0x0b);
        지우기();
    }

    static void 직렬바이트(int uara) {
        int 횟수 = 100000;
        while ((pūkoro_uara.입출력바이트읽기(0x3fd) & 0x20) == 0 && 횟수 > 0) 횟수--;
        if (횟수 > 0) pūkoro_uara.입출력바이트쓰기(0x3f8, uara);
    }

    static void 지우기() {
        for (int INDEX = 0; INDEX < 2000; INDEX++) {
            pūkoro_uara.tuhi_Pūmahara(0xb8000 + INDEX * 2, 32);
            pūkoro_uara.tuhi_Pūmahara(0xb8001 + INDEX * 2, 색);
        }
        kāniwha_tāurunga = 0;
        pehu_uara();
    }

    static void pehu_uara() {
        pūkoro_uara.입출력바이트쓰기(0x3d4, 14);
        pūkoro_uara.입출력바이트쓰기(0x3d5, kāniwha_tāurunga >> 8);
        pūkoro_uara.입출력바이트쓰기(0x3d4, 15);
        pūkoro_uara.입출력바이트쓰기(0x3d5, kāniwha_tāurunga & 255);
    }

    static void 화면문자(int uara) {
        if (uara == 13) return;
        if (uara == 10) {
            kāniwha_tāurunga = (kāniwha_tāurunga / 80 + 1) * 80;
        } else if (uara == 8) {
            if (kāniwha_tāurunga > 0) {
                kāniwha_tāurunga--;
                pūkoro_uara.tuhi_Pūmahara(0xb8000 + kāniwha_tāurunga * 2, 32);
            }
        } else {
            pūkoro_uara.tuhi_Pūmahara(0xb8000 + kāniwha_tāurunga * 2, uara < 128 ? uara : '?');
            pūkoro_uara.tuhi_Pūmahara(0xb8001 + kāniwha_tāurunga * 2, 색);
            kāniwha_tāurunga++;
        }
        if (kāniwha_tāurunga >= 2000) {
            for (int INDEX = 0; INDEX < 3840; INDEX++)
                pūkoro_uara.tuhi_Pūmahara(0xb8000 + INDEX, pūkoro_uara.기억읽기(0xb80a0 + INDEX));
            for (int INDEX = 1920; INDEX < 2000; INDEX++) {
                pūkoro_uara.tuhi_Pūmahara(0xb8000 + INDEX * 2, 32);
                pūkoro_uara.tuhi_Pūmahara(0xb8001 + INDEX * 2, 색);
            }
            kāniwha_tāurunga = 1920;
        }
        pehu_uara();
    }

    static void 문자(int uara) {
        if (uara < 128) {
            if (uara == 10) 직렬바이트(13);
            직렬바이트(uara);
        } else if (uara < 2048) {
            직렬바이트(0xc0 | (uara >> 6));
            직렬바이트(0x80 | (uara & 63));
        } else {
            직렬바이트(0xe0 | (uara >> 12));
            직렬바이트(0x80 | ((uara >> 6) & 63));
            직렬바이트(0x80 | (uara & 63));
        }
        화면문자(uara);
    }

    static void Tuhia(String Ihirangi_uara) {
        for (int INDEX = 0; INDEX < Ihirangi_uara.length(); INDEX++) 문자(Ihirangi_uara.charAt(INDEX));
    }

    static void 수쓰기(int uara) {
        // 양수로 바꾸지 않으므로 Integer.MIN_VALUE도 안전하다.
        if (uara < 0) 문자('-');
        else uara = -uara;
        int tūranga_INDEX = 1000000000;
        boolean whakahaere = false;
        while (tūranga_INDEX > 0) {
            int mati_uara = -(uara / tūranga_INDEX);
            if (mati_uara != 0 || whakahaere || tūranga_INDEX == 1) {
                문자('0' + mati_uara);
                whakahaere = true;
            }
            uara %= tūranga_INDEX;
            tūranga_INDEX /= 10;
        }
    }

    static int 직렬읽기() {
        if ((pūkoro_uara.입출력바이트읽기(0x3fd) & 1) != 0) return pūkoro_uara.입출력바이트읽기(0x3f8);
        return -1;
    }
}
