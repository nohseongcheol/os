// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** COM1 직렬 출력과 VGA 80x25 문자 화면. 한글은 직렬 단말에 UTF-8로 출력한다. */
public final class SMS_Terminal {
    static int espasyo_pagpasok = 0;
    static int 색 = 7;

    static void Ihanda() {
        device_VALUE.입출력바이트쓰기(0x3f9, 0);
        device_VALUE.입출력바이트쓰기(0x3fb, 0x80);
        device_VALUE.입출력바이트쓰기(0x3f8, 1);
        device_VALUE.입출력바이트쓰기(0x3f9, 0);
        device_VALUE.입출력바이트쓰기(0x3fb, 3);
        device_VALUE.입출력바이트쓰기(0x3fa, 0xc7);
        device_VALUE.입출력바이트쓰기(0x3fc, 0x0b);
        burahin_pagpasok();
    }

    static void 직렬바이트(int VALUE) {
        int 횟수 = 100000;
        while ((device_VALUE.입출력바이트읽기(0x3fd) & 0x20) == 0 && 횟수 > 0) 횟수--;
        if (횟수 > 0) device_VALUE.입출력바이트쓰기(0x3f8, VALUE);
    }

    static void burahin_pagpasok() {
        for (int INDEX = 0; INDEX < 2000; INDEX++) {
            device_VALUE.sumulat_Memory(0xb8000 + INDEX * 2, 32);
            device_VALUE.sumulat_Memory(0xb8001 + INDEX * 2, 색);
        }
        espasyo_pagpasok = 0;
        kursor_VALUE();
    }

    static void kursor_VALUE() {
        device_VALUE.입출력바이트쓰기(0x3d4, 14);
        device_VALUE.입출력바이트쓰기(0x3d5, espasyo_pagpasok >> 8);
        device_VALUE.입출력바이트쓰기(0x3d4, 15);
        device_VALUE.입출력바이트쓰기(0x3d5, espasyo_pagpasok & 255);
    }

    static void 화면문자(int VALUE) {
        if (VALUE == 13) return;
        if (VALUE == 10) {
            espasyo_pagpasok = (espasyo_pagpasok / 80 + 1) * 80;
        } else if (VALUE == 8) {
            if (espasyo_pagpasok > 0) {
                espasyo_pagpasok--;
                device_VALUE.sumulat_Memory(0xb8000 + espasyo_pagpasok * 2, 32);
            }
        } else {
            device_VALUE.sumulat_Memory(0xb8000 + espasyo_pagpasok * 2, VALUE < 128 ? VALUE : '?');
            device_VALUE.sumulat_Memory(0xb8001 + espasyo_pagpasok * 2, 색);
            espasyo_pagpasok++;
        }
        if (espasyo_pagpasok >= 2000) {
            for (int INDEX = 0; INDEX < 3840; INDEX++)
                device_VALUE.sumulat_Memory(0xb8000 + INDEX, device_VALUE.기억읽기(0xb80a0 + INDEX));
            for (int INDEX = 1920; INDEX < 2000; INDEX++) {
                device_VALUE.sumulat_Memory(0xb8000 + INDEX * 2, 32);
                device_VALUE.sumulat_Memory(0xb8001 + INDEX * 2, 색);
            }
            espasyo_pagpasok = 1920;
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

    static void sumulat(String Nilalaman_VALUE) {
        for (int INDEX = 0; INDEX < Nilalaman_VALUE.length(); INDEX++) 문자(Nilalaman_VALUE.charAt(INDEX));
    }

    static void 수쓰기(int VALUE) {
        // 양수로 바꾸지 않으므로 Integer.MIN_VALUE도 안전하다.
        if (VALUE < 0) 문자('-');
        else VALUE = -VALUE;
        int posisyon_INDEX = 1000000000;
        boolean run = false;
        while (posisyon_INDEX > 0) {
            int digit_VALUE = -(VALUE / posisyon_INDEX);
            if (digit_VALUE != 0 || run || posisyon_INDEX == 1) {
                문자('0' + digit_VALUE);
                run = true;
            }
            VALUE %= posisyon_INDEX;
            posisyon_INDEX /= 10;
        }
    }

    static int 직렬읽기() {
        if ((device_VALUE.입출력바이트읽기(0x3fd) & 1) != 0) return device_VALUE.입출력바이트읽기(0x3f8);
        return -1;
    }
}
