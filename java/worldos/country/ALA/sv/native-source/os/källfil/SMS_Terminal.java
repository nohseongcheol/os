// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** COM1 직렬 출력과 VGA 80x25 문자 skärmbild. 한글은 직렬 단말에 UTF-8로 출력한다. */
public final class SMS_Terminal {
    static int fack_post = 0;
    static int 색 = 7;

    static void Förbereda() {
        enhet_värde.입출력바이트쓰기(0x3f9, 0);
        enhet_värde.입출력바이트쓰기(0x3fb, 0x80);
        enhet_värde.입출력바이트쓰기(0x3f8, 1);
        enhet_värde.입출력바이트쓰기(0x3f9, 0);
        enhet_värde.입출력바이트쓰기(0x3fb, 3);
        enhet_värde.입출력바이트쓰기(0x3fa, 0xc7);
        enhet_värde.입출력바이트쓰기(0x3fc, 0x0b);
        radera_post();
    }

    static void 직렬바이트(int värde) {
        int repetition_ANTAL = 100000;
        while ((enhet_värde.입출력바이트읽기(0x3fd) & 0x20) == 0 && repetition_ANTAL > 0) repetition_ANTAL--;
        if (repetition_ANTAL > 0) enhet_värde.입출력바이트쓰기(0x3f8, värde);
    }

    static void radera_post() {
        for (int INDEX = 0; INDEX < 2000; INDEX++) {
            enhet_värde.skriva_Minne(0xb8000 + INDEX * 2, 32);
            enhet_värde.skriva_Minne(0xb8001 + INDEX * 2, 색);
        }
        fack_post = 0;
        markör_värde_04ee3e20();
    }

    static void markör_värde_04ee3e20() {
        enhet_värde.입출력바이트쓰기(0x3d4, 14);
        enhet_värde.입출력바이트쓰기(0x3d5, fack_post >> 8);
        enhet_värde.입출력바이트쓰기(0x3d4, 15);
        enhet_värde.입출력바이트쓰기(0x3d5, fack_post & 255);
    }

    static void skärmbild_tecken(int värde) {
        if (värde == 13) return;
        if (värde == 10) {
            fack_post = (fack_post / 80 + 1) * 80;
        } else if (värde == 8) {
            if (fack_post > 0) {
                fack_post--;
                enhet_värde.skriva_Minne(0xb8000 + fack_post * 2, 32);
            }
        } else {
            enhet_värde.skriva_Minne(0xb8000 + fack_post * 2, värde < 128 ? värde : '?');
            enhet_värde.skriva_Minne(0xb8001 + fack_post * 2, 색);
            fack_post++;
        }
        if (fack_post >= 2000) {
            for (int INDEX = 0; INDEX < 3840; INDEX++)
                enhet_värde.skriva_Minne(0xb8000 + INDEX, enhet_värde.läsa_Minne(0xb80a0 + INDEX));
            for (int INDEX = 1920; INDEX < 2000; INDEX++) {
                enhet_värde.skriva_Minne(0xb8000 + INDEX * 2, 32);
                enhet_värde.skriva_Minne(0xb8001 + INDEX * 2, 색);
            }
            fack_post = 1920;
        }
        markör_värde_04ee3e20();
    }

    static void 문자(int värde) {
        if (värde < 128) {
            if (värde == 10) 직렬바이트(13);
            직렬바이트(värde);
        } else if (värde < 2048) {
            직렬바이트(0xc0 | (värde >> 6));
            직렬바이트(0x80 | (värde & 63));
        } else {
            직렬바이트(0xe0 | (värde >> 12));
            직렬바이트(0x80 | ((värde >> 6) & 63));
            직렬바이트(0x80 | (värde & 63));
        }
        skärmbild_tecken(värde);
    }

    static void Skriv(String Innehåll_värde) {
        for (int INDEX = 0; INDEX < Innehåll_värde.length(); INDEX++) 문자(Innehåll_värde.charAt(INDEX));
    }

    static void skriva_nummer(int värde) {
        // 양수로 바꾸지 않으므로 Integer.MIN_VALUE도 안전하다.
        if (värde < 0) 문자('-');
        else värde = -värde;
        int positionsindex = 1000000000;
        boolean Kör = false;
        while (positionsindex > 0) {
            int siffra_värde = -(värde / positionsindex);
            if (siffra_värde != 0 || Kör || positionsindex == 1) {
                문자('0' + siffra_värde);
                Kör = true;
            }
            värde %= positionsindex;
            positionsindex /= 10;
        }
    }

    static int 직렬읽기() {
        if ((enhet_värde.입출력바이트읽기(0x3fd) & 1) != 0) return enhet_värde.입출력바이트읽기(0x3f8);
        return -1;
    }
}
