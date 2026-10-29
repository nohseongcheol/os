// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** COM1 직렬 출력과 VGA 80x25 문자 화면. 한글은 직렬 단말에 UTF-8로 출력한다. */
public final class SMS_Terminal {
    static int 칸 = 0;
    static int 색 = 7;

    static void Pripremi() {
        uređaj_VALUE.입출력바이트쓰기(0x3f9, 0);
        uređaj_VALUE.입출력바이트쓰기(0x3fb, 0x80);
        uređaj_VALUE.입출력바이트쓰기(0x3f8, 1);
        uređaj_VALUE.입출력바이트쓰기(0x3f9, 0);
        uređaj_VALUE.입출력바이트쓰기(0x3fb, 3);
        uređaj_VALUE.입출력바이트쓰기(0x3fa, 0xc7);
        uređaj_VALUE.입출력바이트쓰기(0x3fc, 0x0b);
        izbrisati_unos();
    }

    static void 직렬바이트(int VALUE) {
        int 횟수 = 100000;
        while ((uređaj_VALUE.입출력바이트읽기(0x3fd) & 0x20) == 0 && 횟수 > 0) 횟수--;
        if (횟수 > 0) uređaj_VALUE.입출력바이트쓰기(0x3f8, VALUE);
    }

    static void izbrisati_unos() {
        for (int INDEX = 0; INDEX < 2000; INDEX++) {
            uređaj_VALUE.zapisivanje_Memorija(0xb8000 + INDEX * 2, 32);
            uređaj_VALUE.zapisivanje_Memorija(0xb8001 + INDEX * 2, 색);
        }
        칸 = 0;
        kursor_VALUE();
    }

    static void kursor_VALUE() {
        uređaj_VALUE.입출력바이트쓰기(0x3d4, 14);
        uređaj_VALUE.입출력바이트쓰기(0x3d5, 칸 >> 8);
        uređaj_VALUE.입출력바이트쓰기(0x3d4, 15);
        uređaj_VALUE.입출력바이트쓰기(0x3d5, 칸 & 255);
    }

    static void 화면문자(int VALUE) {
        if (VALUE == 13) return;
        if (VALUE == 10) {
            칸 = (칸 / 80 + 1) * 80;
        } else if (VALUE == 8) {
            if (칸 > 0) {
                칸--;
                uređaj_VALUE.zapisivanje_Memorija(0xb8000 + 칸 * 2, 32);
            }
        } else {
            uređaj_VALUE.zapisivanje_Memorija(0xb8000 + 칸 * 2, VALUE < 128 ? VALUE : '?');
            uređaj_VALUE.zapisivanje_Memorija(0xb8001 + 칸 * 2, 색);
            칸++;
        }
        if (칸 >= 2000) {
            for (int INDEX = 0; INDEX < 3840; INDEX++)
                uređaj_VALUE.zapisivanje_Memorija(0xb8000 + INDEX, uređaj_VALUE.기억읽기(0xb80a0 + INDEX));
            for (int INDEX = 1920; INDEX < 2000; INDEX++) {
                uređaj_VALUE.zapisivanje_Memorija(0xb8000 + INDEX * 2, 32);
                uređaj_VALUE.zapisivanje_Memorija(0xb8001 + INDEX * 2, 색);
            }
            칸 = 1920;
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

    static void Zapisuj(String Sadržaj_VALUE) {
        for (int INDEX = 0; INDEX < Sadržaj_VALUE.length(); INDEX++) 문자(Sadržaj_VALUE.charAt(INDEX));
    }

    static void 수쓰기(int VALUE) {
        // 양수로 바꾸지 않으므로 Integer.MIN_VALUE도 안전하다.
        if (VALUE < 0) 문자('-');
        else VALUE = -VALUE;
        int indeks_položaja = 1000000000;
        boolean Pokreni = false;
        while (indeks_položaja > 0) {
            int znamenka_VALUE = -(VALUE / indeks_položaja);
            if (znamenka_VALUE != 0 || Pokreni || indeks_položaja == 1) {
                문자('0' + znamenka_VALUE);
                Pokreni = true;
            }
            VALUE %= indeks_položaja;
            indeks_položaja /= 10;
        }
    }

    static int 직렬읽기() {
        if ((uređaj_VALUE.입출력바이트읽기(0x3fd) & 1) != 0) return uređaj_VALUE.입출력바이트읽기(0x3f8);
        return -1;
    }
}
