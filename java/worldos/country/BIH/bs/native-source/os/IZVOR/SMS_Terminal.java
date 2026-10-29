// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** COM1 직렬 출력과 VGA 80x25 문자 화면. 한글은 직렬 단말에 UTF-8로 출력한다. */
public final class SMS_Terminal {
    static int prostor_za_unos_unos = 0;
    static int 색 = 7;

    static void Pripremiti() {
        uređaj_VALUE.입출력바이트쓰기(0x3f9, 0);
        uređaj_VALUE.입출력바이트쓰기(0x3fb, 0x80);
        uređaj_VALUE.입출력바이트쓰기(0x3f8, 1);
        uređaj_VALUE.입출력바이트쓰기(0x3f9, 0);
        uređaj_VALUE.입출력바이트쓰기(0x3fb, 3);
        uređaj_VALUE.입출력바이트쓰기(0x3fa, 0xc7);
        uređaj_VALUE.입출력바이트쓰기(0x3fc, 0x0b);
        지우기();
    }

    static void 직렬바이트(int VALUE) {
        int 횟수 = 100000;
        while ((uređaj_VALUE.입출력바이트읽기(0x3fd) & 0x20) == 0 && 횟수 > 0) 횟수--;
        if (횟수 > 0) uređaj_VALUE.입출력바이트쓰기(0x3f8, VALUE);
    }

    static void 지우기() {
        for (int INDEX = 0; INDEX < 2000; INDEX++) {
            uređaj_VALUE.pisati_Memorija(0xb8000 + INDEX * 2, 32);
            uređaj_VALUE.pisati_Memorija(0xb8001 + INDEX * 2, 색);
        }
        prostor_za_unos_unos = 0;
        kursor_VALUE();
    }

    static void kursor_VALUE() {
        uređaj_VALUE.입출력바이트쓰기(0x3d4, 14);
        uređaj_VALUE.입출력바이트쓰기(0x3d5, prostor_za_unos_unos >> 8);
        uređaj_VALUE.입출력바이트쓰기(0x3d4, 15);
        uređaj_VALUE.입출력바이트쓰기(0x3d5, prostor_za_unos_unos & 255);
    }

    static void 화면문자(int VALUE) {
        if (VALUE == 13) return;
        if (VALUE == 10) {
            prostor_za_unos_unos = (prostor_za_unos_unos / 80 + 1) * 80;
        } else if (VALUE == 8) {
            if (prostor_za_unos_unos > 0) {
                prostor_za_unos_unos--;
                uređaj_VALUE.pisati_Memorija(0xb8000 + prostor_za_unos_unos * 2, 32);
            }
        } else {
            uređaj_VALUE.pisati_Memorija(0xb8000 + prostor_za_unos_unos * 2, VALUE < 128 ? VALUE : '?');
            uređaj_VALUE.pisati_Memorija(0xb8001 + prostor_za_unos_unos * 2, 색);
            prostor_za_unos_unos++;
        }
        if (prostor_za_unos_unos >= 2000) {
            for (int INDEX = 0; INDEX < 3840; INDEX++)
                uređaj_VALUE.pisati_Memorija(0xb8000 + INDEX, uređaj_VALUE.기억읽기(0xb80a0 + INDEX));
            for (int INDEX = 1920; INDEX < 2000; INDEX++) {
                uređaj_VALUE.pisati_Memorija(0xb8000 + INDEX * 2, 32);
                uređaj_VALUE.pisati_Memorija(0xb8001 + INDEX * 2, 색);
            }
            prostor_za_unos_unos = 1920;
        }
        kursor_VALUE();
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

    static void Piši(String Sadržaj_VALUE) {
        for (int INDEX = 0; INDEX < Sadržaj_VALUE.length(); INDEX++) 문자(Sadržaj_VALUE.charAt(INDEX));
    }

    static void 수쓰기(int VALUE) {
        // 양수로 바꾸지 않으므로 Integer.MIN_VALUE도 안전하다.
        if (VALUE < 0) 문자('-');
        else VALUE = -VALUE;
        int položaj_INDEX = 1000000000;
        boolean Pokreni = false;
        while (položaj_INDEX > 0) {
            int cifra_VALUE = -(VALUE / položaj_INDEX);
            if (cifra_VALUE != 0 || Pokreni || položaj_INDEX == 1) {
                문자('0' + cifra_VALUE);
                Pokreni = true;
            }
            VALUE %= položaj_INDEX;
            položaj_INDEX /= 10;
        }
    }

    static int 직렬읽기() {
        if ((uređaj_VALUE.입출력바이트읽기(0x3fd) & 1) != 0) return uređaj_VALUE.입출력바이트읽기(0x3f8);
        return -1;
    }
}
