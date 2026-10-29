// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** COM1 직렬 출력과 VGA 80x25 문자 화면. 한글은 직렬 단말에 UTF-8로 출력한다. */
public final class 문자단말 {
    static int umwanya_icyinjizwa = 0;
    static int 색 = 7;

    static void Gutegura() {
        igendanwa_agaciro.입출력바이트쓰기(0x3f9, 0);
        igendanwa_agaciro.입출력바이트쓰기(0x3fb, 0x80);
        igendanwa_agaciro.입출력바이트쓰기(0x3f8, 1);
        igendanwa_agaciro.입출력바이트쓰기(0x3f9, 0);
        igendanwa_agaciro.입출력바이트쓰기(0x3fb, 3);
        igendanwa_agaciro.입출력바이트쓰기(0x3fa, 0xc7);
        igendanwa_agaciro.입출력바이트쓰기(0x3fc, 0x0b);
        지우기();
    }

    static void 직렬바이트(int agaciro) {
        int 횟수 = 100000;
        while ((igendanwa_agaciro.입출력바이트읽기(0x3fd) & 0x20) == 0 && 횟수 > 0) 횟수--;
        if (횟수 > 0) igendanwa_agaciro.입출력바이트쓰기(0x3f8, agaciro);
    }

    static void 지우기() {
        for (int umugerekashakiro = 0; umugerekashakiro < 2000; umugerekashakiro++) {
            igendanwa_agaciro.kwandika_ububiko(0xb8000 + umugerekashakiro * 2, 32);
            igendanwa_agaciro.kwandika_ububiko(0xb8001 + umugerekashakiro * 2, 색);
        }
        umwanya_icyinjizwa = 0;
        inyoboranyandika_agaciro();
    }

    static void inyoboranyandika_agaciro() {
        igendanwa_agaciro.입출력바이트쓰기(0x3d4, 14);
        igendanwa_agaciro.입출력바이트쓰기(0x3d5, umwanya_icyinjizwa >> 8);
        igendanwa_agaciro.입출력바이트쓰기(0x3d4, 15);
        igendanwa_agaciro.입출력바이트쓰기(0x3d5, umwanya_icyinjizwa & 255);
    }

    static void 화면문자(int agaciro) {
        if (agaciro == 13) return;
        if (agaciro == 10) {
            umwanya_icyinjizwa = (umwanya_icyinjizwa / 80 + 1) * 80;
        } else if (agaciro == 8) {
            if (umwanya_icyinjizwa > 0) {
                umwanya_icyinjizwa--;
                igendanwa_agaciro.kwandika_ububiko(0xb8000 + umwanya_icyinjizwa * 2, 32);
            }
        } else {
            igendanwa_agaciro.kwandika_ububiko(0xb8000 + umwanya_icyinjizwa * 2, agaciro < 128 ? agaciro : '?');
            igendanwa_agaciro.kwandika_ububiko(0xb8001 + umwanya_icyinjizwa * 2, 색);
            umwanya_icyinjizwa++;
        }
        if (umwanya_icyinjizwa >= 2000) {
            for (int umugerekashakiro = 0; umugerekashakiro < 3840; umugerekashakiro++)
                igendanwa_agaciro.kwandika_ububiko(0xb8000 + umugerekashakiro, igendanwa_agaciro.기억읽기(0xb80a0 + umugerekashakiro));
            for (int umugerekashakiro = 1920; umugerekashakiro < 2000; umugerekashakiro++) {
                igendanwa_agaciro.kwandika_ububiko(0xb8000 + umugerekashakiro * 2, 32);
                igendanwa_agaciro.kwandika_ububiko(0xb8001 + umugerekashakiro * 2, 색);
            }
            umwanya_icyinjizwa = 1920;
        }
        inyoboranyandika_agaciro();
    }

    static void 문자(int agaciro) {
        if (agaciro < 128) {
            if (agaciro == 10) 직렬바이트(13);
            직렬바이트(agaciro);
        } else if (agaciro < 2048) {
            직렬바이트(0xc0 | (agaciro >> 6));
            직렬바이트(0x80 | (agaciro & 63));
        } else {
            직렬바이트(0xe0 | (agaciro >> 12));
            직렬바이트(0x80 | ((agaciro >> 6) & 63));
            직렬바이트(0x80 | (agaciro & 63));
        }
        화면문자(agaciro);
    }

    static void kwandika(String Ibirimo_agaciro) {
        for (int umugerekashakiro = 0; umugerekashakiro < Ibirimo_agaciro.length(); umugerekashakiro++) 문자(Ibirimo_agaciro.charAt(umugerekashakiro));
    }

    static void 수쓰기(int agaciro) {
        // 양수로 바꾸지 않으므로 Integer.MIN_VALUE도 안전하다.
        if (agaciro < 0) 문자('-');
        else agaciro = -agaciro;
        int 자리 = 1000000000;
        boolean ihuriro = false;
        while (자리 > 0) {
            int umubare_agaciro = -(agaciro / 자리);
            if (umubare_agaciro != 0 || ihuriro || 자리 == 1) {
                문자('0' + umubare_agaciro);
                ihuriro = true;
            }
            agaciro %= 자리;
            자리 /= 10;
        }
    }

    static int 직렬읽기() {
        if ((igendanwa_agaciro.입출력바이트읽기(0x3fd) & 1) != 0) return igendanwa_agaciro.입출력바이트읽기(0x3f8);
        return -1;
    }
}
