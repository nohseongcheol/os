// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** COM1 직렬 출력과 VGA 80x25 문자 화면. 한글은 직렬 단말에 UTF-8로 출력한다. */
public final class SMS_Endastöð {
    static int rauf_færsla = 0;
    static int 색 = 7;

    static void Undirbúa() {
        tæki_VALUE.입출력바이트쓰기(0x3f9, 0);
        tæki_VALUE.입출력바이트쓰기(0x3fb, 0x80);
        tæki_VALUE.입출력바이트쓰기(0x3f8, 1);
        tæki_VALUE.입출력바이트쓰기(0x3f9, 0);
        tæki_VALUE.입출력바이트쓰기(0x3fb, 3);
        tæki_VALUE.입출력바이트쓰기(0x3fa, 0xc7);
        tæki_VALUE.입출력바이트쓰기(0x3fc, 0x0b);
        eyða_færsla();
    }

    static void 직렬바이트(int VALUE) {
        int 횟수 = 100000;
        while ((tæki_VALUE.입출력바이트읽기(0x3fd) & 0x20) == 0 && 횟수 > 0) 횟수--;
        if (횟수 > 0) tæki_VALUE.입출력바이트쓰기(0x3f8, VALUE);
    }

    static void eyða_færsla() {
        for (int INDEX = 0; INDEX < 2000; INDEX++) {
            tæki_VALUE.skrifa_Minni(0xb8000 + INDEX * 2, 32);
            tæki_VALUE.skrifa_Minni(0xb8001 + INDEX * 2, 색);
        }
        rauf_færsla = 0;
        bendill_VALUE();
    }

    static void bendill_VALUE() {
        tæki_VALUE.입출력바이트쓰기(0x3d4, 14);
        tæki_VALUE.입출력바이트쓰기(0x3d5, rauf_færsla >> 8);
        tæki_VALUE.입출력바이트쓰기(0x3d4, 15);
        tæki_VALUE.입출력바이트쓰기(0x3d5, rauf_færsla & 255);
    }

    static void 화면문자(int VALUE) {
        if (VALUE == 13) return;
        if (VALUE == 10) {
            rauf_færsla = (rauf_færsla / 80 + 1) * 80;
        } else if (VALUE == 8) {
            if (rauf_færsla > 0) {
                rauf_færsla--;
                tæki_VALUE.skrifa_Minni(0xb8000 + rauf_færsla * 2, 32);
            }
        } else {
            tæki_VALUE.skrifa_Minni(0xb8000 + rauf_færsla * 2, VALUE < 128 ? VALUE : '?');
            tæki_VALUE.skrifa_Minni(0xb8001 + rauf_færsla * 2, 색);
            rauf_færsla++;
        }
        if (rauf_færsla >= 2000) {
            for (int INDEX = 0; INDEX < 3840; INDEX++)
                tæki_VALUE.skrifa_Minni(0xb8000 + INDEX, tæki_VALUE.기억읽기(0xb80a0 + INDEX));
            for (int INDEX = 1920; INDEX < 2000; INDEX++) {
                tæki_VALUE.skrifa_Minni(0xb8000 + INDEX * 2, 32);
                tæki_VALUE.skrifa_Minni(0xb8001 + INDEX * 2, 색);
            }
            rauf_færsla = 1920;
        }
        bendill_VALUE();
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

    static void Skrift(String Efni_VALUE) {
        for (int INDEX = 0; INDEX < Efni_VALUE.length(); INDEX++) 문자(Efni_VALUE.charAt(INDEX));
    }

    static void skrifa_númer(int VALUE) {
        // 양수로 바꾸지 않으므로 Integer.MIN_VALUE도 안전하다.
        if (VALUE < 0) 문자('-');
        else VALUE = -VALUE;
        int staða_INDEX = 1000000000;
        boolean Keyra_2 = false;
        while (staða_INDEX > 0) {
            int tölustafur_VALUE = -(VALUE / staða_INDEX);
            if (tölustafur_VALUE != 0 || Keyra_2 || staða_INDEX == 1) {
                문자('0' + tölustafur_VALUE);
                Keyra_2 = true;
            }
            VALUE %= staða_INDEX;
            staða_INDEX /= 10;
        }
    }

    static int 직렬읽기() {
        if ((tæki_VALUE.입출력바이트읽기(0x3fd) & 1) != 0) return tæki_VALUE.입출력바이트읽기(0x3f8);
        return -1;
    }
}
