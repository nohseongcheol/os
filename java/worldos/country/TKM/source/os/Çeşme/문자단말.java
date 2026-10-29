// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** COM1 직렬 출력과 VGA 80x25 문자 화면. 한글은 직렬 단말에 UTF-8로 출력한다. */
public final class 문자단말 {
    static int ýer_girizmeklik = 0;
    static int 색 = 7;

    static void Taýýarla() {
        enjam_baha.입출력바이트쓰기(0x3f9, 0);
        enjam_baha.입출력바이트쓰기(0x3fb, 0x80);
        enjam_baha.입출력바이트쓰기(0x3f8, 1);
        enjam_baha.입출력바이트쓰기(0x3f9, 0);
        enjam_baha.입출력바이트쓰기(0x3fb, 3);
        enjam_baha.입출력바이트쓰기(0x3fa, 0xc7);
        enjam_baha.입출력바이트쓰기(0x3fc, 0x0b);
        지우기();
    }

    static void 직렬바이트(int baha) {
        int 횟수 = 100000;
        while ((enjam_baha.입출력바이트읽기(0x3fd) & 0x20) == 0 && 횟수 > 0) 횟수--;
        if (횟수 > 0) enjam_baha.입출력바이트쓰기(0x3f8, baha);
    }

    static void 지우기() {
        for (int indeks = 0; indeks < 2000; indeks++) {
            enjam_baha.ýaz_ýat(0xb8000 + indeks * 2, 32);
            enjam_baha.ýaz_ýat(0xb8001 + indeks * 2, 색);
        }
        ýer_girizmeklik = 0;
        kursor_baha();
    }

    static void kursor_baha() {
        enjam_baha.입출력바이트쓰기(0x3d4, 14);
        enjam_baha.입출력바이트쓰기(0x3d5, ýer_girizmeklik >> 8);
        enjam_baha.입출력바이트쓰기(0x3d4, 15);
        enjam_baha.입출력바이트쓰기(0x3d5, ýer_girizmeklik & 255);
    }

    static void 화면문자(int baha) {
        if (baha == 13) return;
        if (baha == 10) {
            ýer_girizmeklik = (ýer_girizmeklik / 80 + 1) * 80;
        } else if (baha == 8) {
            if (ýer_girizmeklik > 0) {
                ýer_girizmeklik--;
                enjam_baha.ýaz_ýat(0xb8000 + ýer_girizmeklik * 2, 32);
            }
        } else {
            enjam_baha.ýaz_ýat(0xb8000 + ýer_girizmeklik * 2, baha < 128 ? baha : '?');
            enjam_baha.ýaz_ýat(0xb8001 + ýer_girizmeklik * 2, 색);
            ýer_girizmeklik++;
        }
        if (ýer_girizmeklik >= 2000) {
            for (int indeks = 0; indeks < 3840; indeks++)
                enjam_baha.ýaz_ýat(0xb8000 + indeks, enjam_baha.기억읽기(0xb80a0 + indeks));
            for (int indeks = 1920; indeks < 2000; indeks++) {
                enjam_baha.ýaz_ýat(0xb8000 + indeks * 2, 32);
                enjam_baha.ýaz_ýat(0xb8001 + indeks * 2, 색);
            }
            ýer_girizmeklik = 1920;
        }
        kursor_baha();
    }

    static void 문자(int baha) {
        if (baha < 128) {
            if (baha == 10) 직렬바이트(13);
            직렬바이트(baha);
        } else if (baha < 2048) {
            직렬바이트(0xc0 | (baha >> 6));
            직렬바이트(0x80 | (baha & 63));
        } else {
            직렬바이트(0xe0 | (baha >> 12));
            직렬바이트(0x80 | ((baha >> 6) & 63));
            직렬바이트(0x80 | (baha & 63));
        }
        화면문자(baha);
    }

    static void Ýaz(String Mazmun_baha) {
        for (int indeks = 0; indeks < Mazmun_baha.length(); indeks++) 문자(Mazmun_baha.charAt(indeks));
    }

    static void 수쓰기(int baha) {
        // 양수로 바꾸지 않으므로 Integer.MIN_VALUE도 안전하다.
        if (baha < 0) 문자('-');
        else baha = -baha;
        int 자리 = 1000000000;
        boolean Bitir = false;
        while (자리 > 0) {
            int san_baha = -(baha / 자리);
            if (san_baha != 0 || Bitir || 자리 == 1) {
                문자('0' + san_baha);
                Bitir = true;
            }
            baha %= 자리;
            자리 /= 10;
        }
    }

    static int 직렬읽기() {
        if ((enjam_baha.입출력바이트읽기(0x3fd) & 1) != 0) return enjam_baha.입출력바이트읽기(0x3f8);
        return -1;
    }
}
