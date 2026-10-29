// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** COM1 직렬 출력과 VGA 80x25 문자 화면. 한글은 직렬 단말에 UTF-8로 출력한다. */
public final class SMS_Terminal {
    static int felt_oppføring = 0;
    static int 색 = 7;

    static void Klargjer() {
        mobil_VALUE.입출력바이트쓰기(0x3f9, 0);
        mobil_VALUE.입출력바이트쓰기(0x3fb, 0x80);
        mobil_VALUE.입출력바이트쓰기(0x3f8, 1);
        mobil_VALUE.입출력바이트쓰기(0x3f9, 0);
        mobil_VALUE.입출력바이트쓰기(0x3fb, 3);
        mobil_VALUE.입출력바이트쓰기(0x3fa, 0xc7);
        mobil_VALUE.입출력바이트쓰기(0x3fc, 0x0b);
        지우기();
    }

    static void 직렬바이트(int VALUE) {
        int 횟수 = 100000;
        while ((mobil_VALUE.입출력바이트읽기(0x3fd) & 0x20) == 0 && 횟수 > 0) 횟수--;
        if (횟수 > 0) mobil_VALUE.입출력바이트쓰기(0x3f8, VALUE);
    }

    static void 지우기() {
        for (int INDEX = 0; INDEX < 2000; INDEX++) {
            mobil_VALUE.skrive_Minne(0xb8000 + INDEX * 2, 32);
            mobil_VALUE.skrive_Minne(0xb8001 + INDEX * 2, 색);
        }
        felt_oppføring = 0;
        markør_VALUE();
    }

    static void markør_VALUE() {
        mobil_VALUE.입출력바이트쓰기(0x3d4, 14);
        mobil_VALUE.입출력바이트쓰기(0x3d5, felt_oppføring >> 8);
        mobil_VALUE.입출력바이트쓰기(0x3d4, 15);
        mobil_VALUE.입출력바이트쓰기(0x3d5, felt_oppføring & 255);
    }

    static void 화면문자(int VALUE) {
        if (VALUE == 13) return;
        if (VALUE == 10) {
            felt_oppføring = (felt_oppføring / 80 + 1) * 80;
        } else if (VALUE == 8) {
            if (felt_oppføring > 0) {
                felt_oppføring--;
                mobil_VALUE.skrive_Minne(0xb8000 + felt_oppføring * 2, 32);
            }
        } else {
            mobil_VALUE.skrive_Minne(0xb8000 + felt_oppføring * 2, VALUE < 128 ? VALUE : '?');
            mobil_VALUE.skrive_Minne(0xb8001 + felt_oppføring * 2, 색);
            felt_oppføring++;
        }
        if (felt_oppføring >= 2000) {
            for (int INDEX = 0; INDEX < 3840; INDEX++)
                mobil_VALUE.skrive_Minne(0xb8000 + INDEX, mobil_VALUE.기억읽기(0xb80a0 + INDEX));
            for (int INDEX = 1920; INDEX < 2000; INDEX++) {
                mobil_VALUE.skrive_Minne(0xb8000 + INDEX * 2, 32);
                mobil_VALUE.skrive_Minne(0xb8001 + INDEX * 2, 색);
            }
            felt_oppføring = 1920;
        }
        markør_VALUE();
    }

    static void 문자(int VALUE) {
        if (VALUE < 128) {
            if (VALUE == 10) 직렬바이트(13);
            직렬바이트(VALUE);
        } else if (VALUE < 2048) {
            직렬바이트(0xc0 | (VALUE >> 6));
            직렬바이트(0x80 | (VALUE & 63));
        } else {
            직렬바이트(0xe0 | (VALUE >> 12));
            직렬바이트(0x80 | ((VALUE >> 6) & 63));
            직렬바이트(0x80 | (VALUE & 63));
        }
        화면문자(VALUE);
    }

    static void Skriv(String Innhald_VALUE) {
        for (int INDEX = 0; INDEX < Innhald_VALUE.length(); INDEX++) 문자(Innhald_VALUE.charAt(INDEX));
    }

    static void 수쓰기(int VALUE) {
        // 양수로 바꾸지 않으므로 Integer.MIN_VALUE도 안전하다.
        if (VALUE < 0) 문자('-');
        else VALUE = -VALUE;
        int plassere_INDEX = 1000000000;
        boolean Køyr_2 = false;
        while (plassere_INDEX > 0) {
            int siffer_VALUE = -(VALUE / plassere_INDEX);
            if (siffer_VALUE != 0 || Køyr_2 || plassere_INDEX == 1) {
                문자('0' + siffer_VALUE);
                Køyr_2 = true;
            }
            VALUE %= plassere_INDEX;
            plassere_INDEX /= 10;
        }
    }

    static int 직렬읽기() {
        if ((mobil_VALUE.입출력바이트읽기(0x3fd) & 1) != 0) return mobil_VALUE.입출력바이트읽기(0x3f8);
        return -1;
    }
}
