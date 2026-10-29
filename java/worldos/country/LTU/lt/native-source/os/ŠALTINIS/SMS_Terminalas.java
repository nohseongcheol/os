// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** COM1 직렬 출력과 VGA 80x25 문자 화면. 한글은 직렬 단말에 UTF-8로 출력한다. */
public final class SMS_Terminalas {
    static int 칸 = 0;
    static int 색 = 7;

    static void Parengti() {
        įrenginys_VALUE.입출력바이트쓰기(0x3f9, 0);
        įrenginys_VALUE.입출력바이트쓰기(0x3fb, 0x80);
        įrenginys_VALUE.입출력바이트쓰기(0x3f8, 1);
        įrenginys_VALUE.입출력바이트쓰기(0x3f9, 0);
        įrenginys_VALUE.입출력바이트쓰기(0x3fb, 3);
        įrenginys_VALUE.입출력바이트쓰기(0x3fa, 0xc7);
        įrenginys_VALUE.입출력바이트쓰기(0x3fc, 0x0b);
        ištrinti_įrašas();
    }

    static void 직렬바이트(int VALUE) {
        int 횟수 = 100000;
        while ((įrenginys_VALUE.입출력바이트읽기(0x3fd) & 0x20) == 0 && 횟수 > 0) 횟수--;
        if (횟수 > 0) įrenginys_VALUE.입출력바이트쓰기(0x3f8, VALUE);
    }

    static void ištrinti_įrašas() {
        for (int INDEX = 0; INDEX < 2000; INDEX++) {
            įrenginys_VALUE.rašymas_atmintis(0xb8000 + INDEX * 2, 32);
            įrenginys_VALUE.rašymas_atmintis(0xb8001 + INDEX * 2, 색);
        }
        칸 = 0;
        žymiklis_VALUE();
    }

    static void žymiklis_VALUE() {
        įrenginys_VALUE.입출력바이트쓰기(0x3d4, 14);
        įrenginys_VALUE.입출력바이트쓰기(0x3d5, 칸 >> 8);
        įrenginys_VALUE.입출력바이트쓰기(0x3d4, 15);
        įrenginys_VALUE.입출력바이트쓰기(0x3d5, 칸 & 255);
    }

    static void 화면문자(int VALUE) {
        if (VALUE == 13) return;
        if (VALUE == 10) {
            칸 = (칸 / 80 + 1) * 80;
        } else if (VALUE == 8) {
            if (칸 > 0) {
                칸--;
                įrenginys_VALUE.rašymas_atmintis(0xb8000 + 칸 * 2, 32);
            }
        } else {
            įrenginys_VALUE.rašymas_atmintis(0xb8000 + 칸 * 2, VALUE < 128 ? VALUE : '?');
            įrenginys_VALUE.rašymas_atmintis(0xb8001 + 칸 * 2, 색);
            칸++;
        }
        if (칸 >= 2000) {
            for (int INDEX = 0; INDEX < 3840; INDEX++)
                įrenginys_VALUE.rašymas_atmintis(0xb8000 + INDEX, įrenginys_VALUE.기억읽기(0xb80a0 + INDEX));
            for (int INDEX = 1920; INDEX < 2000; INDEX++) {
                įrenginys_VALUE.rašymas_atmintis(0xb8000 + INDEX * 2, 32);
                įrenginys_VALUE.rašymas_atmintis(0xb8001 + INDEX * 2, 색);
            }
            칸 = 1920;
        }
        žymiklis_VALUE();
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

    static void Rašymas(String Turinys_VALUE) {
        for (int INDEX = 0; INDEX < Turinys_VALUE.length(); INDEX++) 문자(Turinys_VALUE.charAt(INDEX));
    }

    static void rašymas_numeris(int VALUE) {
        // 양수로 바꾸지 않으므로 Integer.MIN_VALUE도 안전하다.
        if (VALUE < 0) 문자('-');
        else VALUE = -VALUE;
        int vietos_rodyklė = 1000000000;
        boolean Paleisti = false;
        while (vietos_rodyklė > 0) {
            int skaitmuo_VALUE = -(VALUE / vietos_rodyklė);
            if (skaitmuo_VALUE != 0 || Paleisti || vietos_rodyklė == 1) {
                문자('0' + skaitmuo_VALUE);
                Paleisti = true;
            }
            VALUE %= vietos_rodyklė;
            vietos_rodyklė /= 10;
        }
    }

    static int 직렬읽기() {
        if ((įrenginys_VALUE.입출력바이트읽기(0x3fd) & 1) != 0) return įrenginys_VALUE.입출력바이트읽기(0x3f8);
        return -1;
    }
}
