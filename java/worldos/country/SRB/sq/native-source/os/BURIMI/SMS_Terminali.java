// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** COM1 직렬 출력과 VGA 80x25 문자 화면. 한글은 직렬 단말에 UTF-8로 출력한다. */
public final class SMS_Terminali {
    static int hapësirë_për_tekst_futje = 0;
    static int 색 = 7;

    static void Përgatit() {
        pajisje_VALUE.입출력바이트쓰기(0x3f9, 0);
        pajisje_VALUE.입출력바이트쓰기(0x3fb, 0x80);
        pajisje_VALUE.입출력바이트쓰기(0x3f8, 1);
        pajisje_VALUE.입출력바이트쓰기(0x3f9, 0);
        pajisje_VALUE.입출력바이트쓰기(0x3fb, 3);
        pajisje_VALUE.입출력바이트쓰기(0x3fa, 0xc7);
        pajisje_VALUE.입출력바이트쓰기(0x3fc, 0x0b);
        spastroj_futje();
    }

    static void 직렬바이트(int VALUE) {
        int 횟수 = 100000;
        while ((pajisje_VALUE.입출력바이트읽기(0x3fd) & 0x20) == 0 && 횟수 > 0) 횟수--;
        if (횟수 > 0) pajisje_VALUE.입출력바이트쓰기(0x3f8, VALUE);
    }

    static void spastroj_futje() {
        for (int INDEX = 0; INDEX < 2000; INDEX++) {
            pajisje_VALUE.shkruaj_Memorie(0xb8000 + INDEX * 2, 32);
            pajisje_VALUE.shkruaj_Memorie(0xb8001 + INDEX * 2, 색);
        }
        hapësirë_për_tekst_futje = 0;
        kursor_VALUE();
    }

    static void kursor_VALUE() {
        pajisje_VALUE.입출력바이트쓰기(0x3d4, 14);
        pajisje_VALUE.입출력바이트쓰기(0x3d5, hapësirë_për_tekst_futje >> 8);
        pajisje_VALUE.입출력바이트쓰기(0x3d4, 15);
        pajisje_VALUE.입출력바이트쓰기(0x3d5, hapësirë_për_tekst_futje & 255);
    }

    static void 화면문자(int VALUE) {
        if (VALUE == 13) return;
        if (VALUE == 10) {
            hapësirë_për_tekst_futje = (hapësirë_për_tekst_futje / 80 + 1) * 80;
        } else if (VALUE == 8) {
            if (hapësirë_për_tekst_futje > 0) {
                hapësirë_për_tekst_futje--;
                pajisje_VALUE.shkruaj_Memorie(0xb8000 + hapësirë_për_tekst_futje * 2, 32);
            }
        } else {
            pajisje_VALUE.shkruaj_Memorie(0xb8000 + hapësirë_për_tekst_futje * 2, VALUE < 128 ? VALUE : '?');
            pajisje_VALUE.shkruaj_Memorie(0xb8001 + hapësirë_për_tekst_futje * 2, 색);
            hapësirë_për_tekst_futje++;
        }
        if (hapësirë_për_tekst_futje >= 2000) {
            for (int INDEX = 0; INDEX < 3840; INDEX++)
                pajisje_VALUE.shkruaj_Memorie(0xb8000 + INDEX, pajisje_VALUE.기억읽기(0xb80a0 + INDEX));
            for (int INDEX = 1920; INDEX < 2000; INDEX++) {
                pajisje_VALUE.shkruaj_Memorie(0xb8000 + INDEX * 2, 32);
                pajisje_VALUE.shkruaj_Memorie(0xb8001 + INDEX * 2, 색);
            }
            hapësirë_për_tekst_futje = 1920;
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

    static void Shkrimi(String Përmbajtje_VALUE) {
        for (int INDEX = 0; INDEX < Përmbajtje_VALUE.length(); INDEX++) 문자(Përmbajtje_VALUE.charAt(INDEX));
    }

    static void 수쓰기(int VALUE) {
        // 양수로 바꾸지 않으므로 Integer.MIN_VALUE도 안전하다.
        if (VALUE < 0) 문자('-');
        else VALUE = -VALUE;
        int pozicioni_INDEX = 1000000000;
        boolean Ekzekuto = false;
        while (pozicioni_INDEX > 0) {
            int shifër_VALUE = -(VALUE / pozicioni_INDEX);
            if (shifër_VALUE != 0 || Ekzekuto || pozicioni_INDEX == 1) {
                문자('0' + shifër_VALUE);
                Ekzekuto = true;
            }
            VALUE %= pozicioni_INDEX;
            pozicioni_INDEX /= 10;
        }
    }

    static int 직렬읽기() {
        if ((pajisje_VALUE.입출력바이트읽기(0x3fd) & 1) != 0) return pajisje_VALUE.입출력바이트읽기(0x3f8);
        return -1;
    }
}
