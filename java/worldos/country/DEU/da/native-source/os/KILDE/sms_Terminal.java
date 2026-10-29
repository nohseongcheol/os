// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** COM1 직렬 출력과 VGA 80x25 문자 skærmbillede. 한글은 직렬 단말에 UTF-8로 출력한다. */
public final class sms_Terminal {
    static int udvidelsesstik_post = 0;
    static int 색 = 7;

    static void Tilrettelæg() {
        enhed_VÆRDI.입출력바이트쓰기(0x3f9, 0);
        enhed_VÆRDI.입출력바이트쓰기(0x3fb, 0x80);
        enhed_VÆRDI.입출력바이트쓰기(0x3f8, 1);
        enhed_VÆRDI.입출력바이트쓰기(0x3f9, 0);
        enhed_VÆRDI.입출력바이트쓰기(0x3fb, 3);
        enhed_VÆRDI.입출력바이트쓰기(0x3fa, 0xc7);
        enhed_VÆRDI.입출력바이트쓰기(0x3fc, 0x0b);
        slette_post();
    }

    static void 직렬바이트(int VÆRDI) {
        int gentagelse_TÆL = 100000;
        while ((enhed_VÆRDI.입출력바이트읽기(0x3fd) & 0x20) == 0 && gentagelse_TÆL > 0) gentagelse_TÆL--;
        if (gentagelse_TÆL > 0) enhed_VÆRDI.입출력바이트쓰기(0x3f8, VÆRDI);
    }

    static void slette_post() {
        for (int INDEKS = 0; INDEKS < 2000; INDEKS++) {
            enhed_VÆRDI.skrive_Hukommelse(0xb8000 + INDEKS * 2, 32);
            enhed_VÆRDI.skrive_Hukommelse(0xb8001 + INDEKS * 2, 색);
        }
        udvidelsesstik_post = 0;
        markør_VÆRDI();
    }

    static void markør_VÆRDI() {
        enhed_VÆRDI.입출력바이트쓰기(0x3d4, 14);
        enhed_VÆRDI.입출력바이트쓰기(0x3d5, udvidelsesstik_post >> 8);
        enhed_VÆRDI.입출력바이트쓰기(0x3d4, 15);
        enhed_VÆRDI.입출력바이트쓰기(0x3d5, udvidelsesstik_post & 255);
    }

    static void skærmbillede_tegn(int VÆRDI) {
        if (VÆRDI == 13) return;
        if (VÆRDI == 10) {
            udvidelsesstik_post = (udvidelsesstik_post / 80 + 1) * 80;
        } else if (VÆRDI == 8) {
            if (udvidelsesstik_post > 0) {
                udvidelsesstik_post--;
                enhed_VÆRDI.skrive_Hukommelse(0xb8000 + udvidelsesstik_post * 2, 32);
            }
        } else {
            enhed_VÆRDI.skrive_Hukommelse(0xb8000 + udvidelsesstik_post * 2, VÆRDI < 128 ? VÆRDI : '?');
            enhed_VÆRDI.skrive_Hukommelse(0xb8001 + udvidelsesstik_post * 2, 색);
            udvidelsesstik_post++;
        }
        if (udvidelsesstik_post >= 2000) {
            for (int INDEKS = 0; INDEKS < 3840; INDEKS++)
                enhed_VÆRDI.skrive_Hukommelse(0xb8000 + INDEKS, enhed_VÆRDI.기억읽기(0xb80a0 + INDEKS));
            for (int INDEKS = 1920; INDEKS < 2000; INDEKS++) {
                enhed_VÆRDI.skrive_Hukommelse(0xb8000 + INDEKS * 2, 32);
                enhed_VÆRDI.skrive_Hukommelse(0xb8001 + INDEKS * 2, 색);
            }
            udvidelsesstik_post = 1920;
        }
        markør_VÆRDI();
    }

    static void 문자(int VÆRDI) {
        if (VÆRDI < 128) {
            if (VÆRDI == 10) 직렬바이트(13);
            직렬바이트(VÆRDI);
        } else if (VÆRDI < 2048) {
            직렬바이트(0xc0 | (VÆRDI >> 6));
            직렬바이트(0x80 | (VÆRDI & 63));
        } else {
            직렬바이트(0xe0 | (VÆRDI >> 12));
            직렬바이트(0x80 | ((VÆRDI >> 6) & 63));
            직렬바이트(0x80 | (VÆRDI & 63));
        }
        skærmbillede_tegn(VÆRDI);
    }

    static void Skrive(String Indhold_VÆRDI) {
        for (int INDEKS = 0; INDEKS < Indhold_VÆRDI.length(); INDEKS++) 문자(Indhold_VÆRDI.charAt(INDEKS));
    }

    static void skrive_tal(int VÆRDI) {
        // 양수로 바꾸지 않으므로 Integer.MIN_VALUE도 안전하다.
        if (VÆRDI < 0) 문자('-');
        else VÆRDI = -VÆRDI;
        int positionsindeks = 1000000000;
        boolean Kør_2 = false;
        while (positionsindeks > 0) {
            int ciffer_VÆRDI = -(VÆRDI / positionsindeks);
            if (ciffer_VÆRDI != 0 || Kør_2 || positionsindeks == 1) {
                문자('0' + ciffer_VÆRDI);
                Kør_2 = true;
            }
            VÆRDI %= positionsindeks;
            positionsindeks /= 10;
        }
    }

    static int 직렬읽기() {
        if ((enhed_VÆRDI.입출력바이트읽기(0x3fd) & 1) != 0) return enhed_VÆRDI.입출력바이트읽기(0x3f8);
        return -1;
    }
}
