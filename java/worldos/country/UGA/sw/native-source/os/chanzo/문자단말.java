// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** COM1 직렬 출력과 VGA 80x25 문자 화면. 한글은 직렬 단말에 UTF-8로 출력한다. */
public final class 문자단말 {
    static int Sloti_ingizo = 0;
    static int 색 = 7;

    static void Andaa() {
        kifaa_thamani.입출력바이트쓰기(0x3f9, 0);
        kifaa_thamani.입출력바이트쓰기(0x3fb, 0x80);
        kifaa_thamani.입출력바이트쓰기(0x3f8, 1);
        kifaa_thamani.입출력바이트쓰기(0x3f9, 0);
        kifaa_thamani.입출력바이트쓰기(0x3fb, 3);
        kifaa_thamani.입출력바이트쓰기(0x3fa, 0xc7);
        kifaa_thamani.입출력바이트쓰기(0x3fc, 0x0b);
        futa_ingizo();
    }

    static void 직렬바이트(int thamani) {
        int 횟수 = 100000;
        while ((kifaa_thamani.입출력바이트읽기(0x3fd) & 0x20) == 0 && 횟수 > 0) 횟수--;
        if (횟수 > 0) kifaa_thamani.입출력바이트쓰기(0x3f8, thamani);
    }

    static void futa_ingizo() {
        for (int kielezo = 0; kielezo < 2000; kielezo++) {
            kifaa_thamani.andika_kumbukumbu(0xb8000 + kielezo * 2, 32);
            kifaa_thamani.andika_kumbukumbu(0xb8001 + kielezo * 2, 색);
        }
        Sloti_ingizo = 0;
        kielekezi_thamani();
    }

    static void kielekezi_thamani() {
        kifaa_thamani.입출력바이트쓰기(0x3d4, 14);
        kifaa_thamani.입출력바이트쓰기(0x3d5, Sloti_ingizo >> 8);
        kifaa_thamani.입출력바이트쓰기(0x3d4, 15);
        kifaa_thamani.입출력바이트쓰기(0x3d5, Sloti_ingizo & 255);
    }

    static void 화면문자(int thamani) {
        if (thamani == 13) return;
        if (thamani == 10) {
            Sloti_ingizo = (Sloti_ingizo / 80 + 1) * 80;
        } else if (thamani == 8) {
            if (Sloti_ingizo > 0) {
                Sloti_ingizo--;
                kifaa_thamani.andika_kumbukumbu(0xb8000 + Sloti_ingizo * 2, 32);
            }
        } else {
            kifaa_thamani.andika_kumbukumbu(0xb8000 + Sloti_ingizo * 2, thamani < 128 ? thamani : '?');
            kifaa_thamani.andika_kumbukumbu(0xb8001 + Sloti_ingizo * 2, 색);
            Sloti_ingizo++;
        }
        if (Sloti_ingizo >= 2000) {
            for (int kielezo = 0; kielezo < 3840; kielezo++)
                kifaa_thamani.andika_kumbukumbu(0xb8000 + kielezo, kifaa_thamani.기억읽기(0xb80a0 + kielezo));
            for (int kielezo = 1920; kielezo < 2000; kielezo++) {
                kifaa_thamani.andika_kumbukumbu(0xb8000 + kielezo * 2, 32);
                kifaa_thamani.andika_kumbukumbu(0xb8001 + kielezo * 2, 색);
            }
            Sloti_ingizo = 1920;
        }
        kielekezi_thamani();
    }

    static void 문자(int thamani) {
        if (thamani < 128) {
            if (thamani == 10) 직렬바이트(13);
            직렬바이트(thamani);
        } else if (thamani < 2048) {
            직렬바이트(0xc0 | (thamani >> 6));
            직렬바이트(0x80 | (thamani & 63));
        } else {
            직렬바이트(0xe0 | (thamani >> 12));
            직렬바이트(0x80 | ((thamani >> 6) & 63));
            직렬바이트(0x80 | (thamani & 63));
        }
        화면문자(thamani);
    }

    static void andika(String maudhui_thamani) {
        for (int kielezo = 0; kielezo < maudhui_thamani.length(); kielezo++) 문자(maudhui_thamani.charAt(kielezo));
    }

    static void 수쓰기(int thamani) {
        // 양수로 바꾸지 않으므로 Integer.MIN_VALUE도 안전하다.
        if (thamani < 0) 문자('-');
        else thamani = -thamani;
        int 자리 = 1000000000;
        boolean endesha = false;
        while (자리 > 0) {
            int dijiti_thamani = -(thamani / 자리);
            if (dijiti_thamani != 0 || endesha || 자리 == 1) {
                문자('0' + dijiti_thamani);
                endesha = true;
            }
            thamani %= 자리;
            자리 /= 10;
        }
    }

    static int 직렬읽기() {
        if ((kifaa_thamani.입출력바이트읽기(0x3fd) & 1) != 0) return kifaa_thamani.입출력바이트읽기(0x3f8);
        return -1;
    }
}
