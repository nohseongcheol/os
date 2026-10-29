// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** COM1 직렬 출력과 VGA 80x25 문자 skjermbilde. 한글은 직렬 단말에 UTF-8로 출력한다. */
public final class SMS_Terminal {
    static int åpning_oppføring = 0;
    static int 색 = 7;

    static void Forbered() {
        enhet_VERDI.입출력바이트쓰기(0x3f9, 0);
        enhet_VERDI.입출력바이트쓰기(0x3fb, 0x80);
        enhet_VERDI.입출력바이트쓰기(0x3f8, 1);
        enhet_VERDI.입출력바이트쓰기(0x3f9, 0);
        enhet_VERDI.입출력바이트쓰기(0x3fb, 3);
        enhet_VERDI.입출력바이트쓰기(0x3fa, 0xc7);
        enhet_VERDI.입출력바이트쓰기(0x3fc, 0x0b);
        slette_oppføring();
    }

    static void 직렬바이트(int VERDI) {
        int 횟수 = 100000;
        while ((enhet_VERDI.입출력바이트읽기(0x3fd) & 0x20) == 0 && 횟수 > 0) 횟수--;
        if (횟수 > 0) enhet_VERDI.입출력바이트쓰기(0x3f8, VERDI);
    }

    static void slette_oppføring() {
        for (int INDEKS = 0; INDEKS < 2000; INDEKS++) {
            enhet_VERDI.skrive_Minne(0xb8000 + INDEKS * 2, 32);
            enhet_VERDI.skrive_Minne(0xb8001 + INDEKS * 2, 색);
        }
        åpning_oppføring = 0;
        markør_VERDI();
    }

    static void markør_VERDI() {
        enhet_VERDI.입출력바이트쓰기(0x3d4, 14);
        enhet_VERDI.입출력바이트쓰기(0x3d5, åpning_oppføring >> 8);
        enhet_VERDI.입출력바이트쓰기(0x3d4, 15);
        enhet_VERDI.입출력바이트쓰기(0x3d5, åpning_oppføring & 255);
    }

    static void skjermbilde_tegn(int VERDI) {
        if (VERDI == 13) return;
        if (VERDI == 10) {
            åpning_oppføring = (åpning_oppføring / 80 + 1) * 80;
        } else if (VERDI == 8) {
            if (åpning_oppføring > 0) {
                åpning_oppføring--;
                enhet_VERDI.skrive_Minne(0xb8000 + åpning_oppføring * 2, 32);
            }
        } else {
            enhet_VERDI.skrive_Minne(0xb8000 + åpning_oppføring * 2, VERDI < 128 ? VERDI : '?');
            enhet_VERDI.skrive_Minne(0xb8001 + åpning_oppføring * 2, 색);
            åpning_oppføring++;
        }
        if (åpning_oppføring >= 2000) {
            for (int INDEKS = 0; INDEKS < 3840; INDEKS++)
                enhet_VERDI.skrive_Minne(0xb8000 + INDEKS, enhet_VERDI.기억읽기(0xb80a0 + INDEKS));
            for (int INDEKS = 1920; INDEKS < 2000; INDEKS++) {
                enhet_VERDI.skrive_Minne(0xb8000 + INDEKS * 2, 32);
                enhet_VERDI.skrive_Minne(0xb8001 + INDEKS * 2, 색);
            }
            åpning_oppføring = 1920;
        }
        markør_VERDI();
    }

    static void 문자(int VERDI) {
        if (VERDI < 128) {
            if (VERDI == 10) 직렬바이트(13);
            직렬바이트(VERDI);
        } else if (VERDI < 2048) {
            직렬바이트(0xc0 | (VERDI >> 6));
            직렬바이트(0x80 | (VERDI & 63));
        } else {
            직렬바이트(0xe0 | (VERDI >> 12));
            직렬바이트(0x80 | ((VERDI >> 6) & 63));
            직렬바이트(0x80 | (VERDI & 63));
        }
        skjermbilde_tegn(VERDI);
    }

    static void Skriv(String Innhold_VERDI) {
        for (int INDEKS = 0; INDEKS < Innhold_VERDI.length(); INDEKS++) 문자(Innhold_VERDI.charAt(INDEKS));
    }

    static void skrive_nummer(int VERDI) {
        // 양수로 바꾸지 않으므로 Integer.MIN_VALUE도 안전하다.
        if (VERDI < 0) 문자('-');
        else VERDI = -VERDI;
        int posisjonsindeks = 1000000000;
        boolean Kjør_2 = false;
        while (posisjonsindeks > 0) {
            int siffer_VERDI = -(VERDI / posisjonsindeks);
            if (siffer_VERDI != 0 || Kjør_2 || posisjonsindeks == 1) {
                문자('0' + siffer_VERDI);
                Kjør_2 = true;
            }
            VERDI %= posisjonsindeks;
            posisjonsindeks /= 10;
        }
    }

    static int 직렬읽기() {
        if ((enhet_VERDI.입출력바이트읽기(0x3fd) & 1) != 0) return enhet_VERDI.입출력바이트읽기(0x3f8);
        return -1;
    }
}
