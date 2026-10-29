// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** COM1 직렬 출력과 VGA 80x25 문자 화면. 한글은 직렬 단말에 UTF-8로 출력한다. */
public final class 문자단말 {
    static int isikhala_okufakwayo = 0;
    static int 색 = 7;

    static void Hlela() {
        idivayisi_inani.입출력바이트쓰기(0x3f9, 0);
        idivayisi_inani.입출력바이트쓰기(0x3fb, 0x80);
        idivayisi_inani.입출력바이트쓰기(0x3f8, 1);
        idivayisi_inani.입출력바이트쓰기(0x3f9, 0);
        idivayisi_inani.입출력바이트쓰기(0x3fb, 3);
        idivayisi_inani.입출력바이트쓰기(0x3fa, 0xc7);
        idivayisi_inani.입출력바이트쓰기(0x3fc, 0x0b);
        지우기();
    }

    static void 직렬바이트(int inani) {
        int 횟수 = 100000;
        while ((idivayisi_inani.입출력바이트읽기(0x3fd) & 0x20) == 0 && 횟수 > 0) 횟수--;
        if (횟수 > 0) idivayisi_inani.입출력바이트쓰기(0x3f8, inani);
    }

    static void 지우기() {
        for (int thola_inkomba = 0; thola_inkomba < 2000; thola_inkomba++) {
            idivayisi_inani.bhala_inkumbulo(0xb8000 + thola_inkomba * 2, 32);
            idivayisi_inani.bhala_inkumbulo(0xb8001 + thola_inkomba * 2, 색);
        }
        isikhala_okufakwayo = 0;
        isikhombisi_inani();
    }

    static void isikhombisi_inani() {
        idivayisi_inani.입출력바이트쓰기(0x3d4, 14);
        idivayisi_inani.입출력바이트쓰기(0x3d5, isikhala_okufakwayo >> 8);
        idivayisi_inani.입출력바이트쓰기(0x3d4, 15);
        idivayisi_inani.입출력바이트쓰기(0x3d5, isikhala_okufakwayo & 255);
    }

    static void 화면문자(int inani) {
        if (inani == 13) return;
        if (inani == 10) {
            isikhala_okufakwayo = (isikhala_okufakwayo / 80 + 1) * 80;
        } else if (inani == 8) {
            if (isikhala_okufakwayo > 0) {
                isikhala_okufakwayo--;
                idivayisi_inani.bhala_inkumbulo(0xb8000 + isikhala_okufakwayo * 2, 32);
            }
        } else {
            idivayisi_inani.bhala_inkumbulo(0xb8000 + isikhala_okufakwayo * 2, inani < 128 ? inani : '?');
            idivayisi_inani.bhala_inkumbulo(0xb8001 + isikhala_okufakwayo * 2, 색);
            isikhala_okufakwayo++;
        }
        if (isikhala_okufakwayo >= 2000) {
            for (int thola_inkomba = 0; thola_inkomba < 3840; thola_inkomba++)
                idivayisi_inani.bhala_inkumbulo(0xb8000 + thola_inkomba, idivayisi_inani.기억읽기(0xb80a0 + thola_inkomba));
            for (int thola_inkomba = 1920; thola_inkomba < 2000; thola_inkomba++) {
                idivayisi_inani.bhala_inkumbulo(0xb8000 + thola_inkomba * 2, 32);
                idivayisi_inani.bhala_inkumbulo(0xb8001 + thola_inkomba * 2, 색);
            }
            isikhala_okufakwayo = 1920;
        }
        isikhombisi_inani();
    }

    static void 문자(int inani) {
        if (inani < 128) {
            if (inani == 10) 직렬바이트(13);
            직렬바이트(inani);
        } else if (inani < 2048) {
            직렬바이트(0xc0 | (inani >> 6));
            직렬바이트(0x80 | (inani & 63));
        } else {
            직렬바이트(0xe0 | (inani >> 12));
            직렬바이트(0x80 | ((inani >> 6) & 63));
            직렬바이트(0x80 | (inani & 63));
        }
        화면문자(inani);
    }

    static void Bhala(String Okuqukethwe_inani) {
        for (int thola_inkomba = 0; thola_inkomba < Okuqukethwe_inani.length(); thola_inkomba++) 문자(Okuqukethwe_inani.charAt(thola_inkomba));
    }

    static void 수쓰기(int inani) {
        // 양수로 바꾸지 않으므로 Integer.MIN_VALUE도 안전하다.
        if (inani < 0) 문자('-');
        else inani = -inani;
        int 자리 = 1000000000;
        boolean Sebenzisa = false;
        while (자리 > 0) {
            int idijithi_inani = -(inani / 자리);
            if (idijithi_inani != 0 || Sebenzisa || 자리 == 1) {
                문자('0' + idijithi_inani);
                Sebenzisa = true;
            }
            inani %= 자리;
            자리 /= 10;
        }
    }

    static int 직렬읽기() {
        if ((idivayisi_inani.입출력바이트읽기(0x3fd) & 1) != 0) return idivayisi_inani.입출력바이트읽기(0x3f8);
        return -1;
    }
}
