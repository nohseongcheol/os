// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** COM1 직렬 출력과 VGA 80x25 문자 화면. 한글은 직렬 단말에 UTF-8로 출력한다. */
public final class SMS_Terfynell {
    static int slot_cofnod = 0;
    static int 색 = 7;

    static void Paratoi() {
        dyfais_VALUE.입출력바이트쓰기(0x3f9, 0);
        dyfais_VALUE.입출력바이트쓰기(0x3fb, 0x80);
        dyfais_VALUE.입출력바이트쓰기(0x3f8, 1);
        dyfais_VALUE.입출력바이트쓰기(0x3f9, 0);
        dyfais_VALUE.입출력바이트쓰기(0x3fb, 3);
        dyfais_VALUE.입출력바이트쓰기(0x3fa, 0xc7);
        dyfais_VALUE.입출력바이트쓰기(0x3fc, 0x0b);
        지우기();
    }

    static void 직렬바이트(int VALUE) {
        int 횟수 = 100000;
        while ((dyfais_VALUE.입출력바이트읽기(0x3fd) & 0x20) == 0 && 횟수 > 0) 횟수--;
        if (횟수 > 0) dyfais_VALUE.입출력바이트쓰기(0x3f8, VALUE);
    }

    static void 지우기() {
        for (int INDEX = 0; INDEX < 2000; INDEX++) {
            dyfais_VALUE.ysgrifennu_Cof(0xb8000 + INDEX * 2, 32);
            dyfais_VALUE.ysgrifennu_Cof(0xb8001 + INDEX * 2, 색);
        }
        slot_cofnod = 0;
        cyrchwr_VALUE();
    }

    static void cyrchwr_VALUE() {
        dyfais_VALUE.입출력바이트쓰기(0x3d4, 14);
        dyfais_VALUE.입출력바이트쓰기(0x3d5, slot_cofnod >> 8);
        dyfais_VALUE.입출력바이트쓰기(0x3d4, 15);
        dyfais_VALUE.입출력바이트쓰기(0x3d5, slot_cofnod & 255);
    }

    static void 화면문자(int VALUE) {
        if (VALUE == 13) return;
        if (VALUE == 10) {
            slot_cofnod = (slot_cofnod / 80 + 1) * 80;
        } else if (VALUE == 8) {
            if (slot_cofnod > 0) {
                slot_cofnod--;
                dyfais_VALUE.ysgrifennu_Cof(0xb8000 + slot_cofnod * 2, 32);
            }
        } else {
            dyfais_VALUE.ysgrifennu_Cof(0xb8000 + slot_cofnod * 2, VALUE < 128 ? VALUE : '?');
            dyfais_VALUE.ysgrifennu_Cof(0xb8001 + slot_cofnod * 2, 색);
            slot_cofnod++;
        }
        if (slot_cofnod >= 2000) {
            for (int INDEX = 0; INDEX < 3840; INDEX++)
                dyfais_VALUE.ysgrifennu_Cof(0xb8000 + INDEX, dyfais_VALUE.기억읽기(0xb80a0 + INDEX));
            for (int INDEX = 1920; INDEX < 2000; INDEX++) {
                dyfais_VALUE.ysgrifennu_Cof(0xb8000 + INDEX * 2, 32);
                dyfais_VALUE.ysgrifennu_Cof(0xb8001 + INDEX * 2, 색);
            }
            slot_cofnod = 1920;
        }
        cyrchwr_VALUE();
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

    static void Ysgrifennu(String Cynnwys_VALUE) {
        for (int INDEX = 0; INDEX < Cynnwys_VALUE.length(); INDEX++) 문자(Cynnwys_VALUE.charAt(INDEX));
    }

    static void 수쓰기(int VALUE) {
        // 양수로 바꾸지 않으므로 Integer.MIN_VALUE도 안전하다.
        if (VALUE < 0) 문자('-');
        else VALUE = -VALUE;
        int safle_INDEX = 1000000000;
        boolean Gweithredu_2 = false;
        while (safle_INDEX > 0) {
            int digid_VALUE = -(VALUE / safle_INDEX);
            if (digid_VALUE != 0 || Gweithredu_2 || safle_INDEX == 1) {
                문자('0' + digid_VALUE);
                Gweithredu_2 = true;
            }
            VALUE %= safle_INDEX;
            safle_INDEX /= 10;
        }
    }

    static int 직렬읽기() {
        if ((dyfais_VALUE.입출력바이트읽기(0x3fd) & 1) != 0) return dyfais_VALUE.입출력바이트읽기(0x3f8);
        return -1;
    }
}
